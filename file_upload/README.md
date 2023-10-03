# P2P Mommy Plus:

## Release Version(2023-10-02):

## Feature Overview:
### Enable OTEL tracers for service, repositories and infrastructure layers:
#### API CHECK LIST(ENABLE MONITORING):

- [x] Auth `prefix=/auth`
  - [x] **POST** `/auth/sms_service/verify` [verify otp after register phone number]
  - [x] **POST** `auth/register` [register with phone number(do before verify otp)]
  - [x] **POST** `auth/sms_service/send-otp` [send otp to login]
  - [ ] **GET** `auth/refresh?device_id={string}&app_version={string}` [refresh token]
  - [x] **POST** `auth/facebook` [login facebook]
  - [x] **POST** `/auth/login` [login with mobile]
  - [ ] **GET** `auth/token-status?app_version={string}` [check token status]
- [ ] Users `prefix=/users`
  - [ ] **PATCH** `users/profile` [complete user profile]
  - [ ] **PATCH** `users/language` [Update UserLanguage]
  - [ ] **POST** `users/avatar/upload` [Upload user avatar]
  - [ ] **PATCH** `users/update-completed-guided-tour` [user complete guide tour]
  - [ ] **POST** `users/send-invite-partner` [Send invite partner] 
  - [ ] **DELETE** `users/remove-partner` [Remove partner]
- [ ] Articles `prefix=/articles`
  - [x] **GET** `articles/article-for-you` [Get List Article for you]
  - [ ] **GET** `articles/banners?bannerType={string}` [Get banner by banner type]

Note: *All Incoming request will go through gin middleware recorded by default*  💾 

#### Config traces & metric provider (Jeager and Prometheus)

Env Variable:
- `OTEL_EXPORTER_ENDPOINT`: OTLP grpc protocol for otel collector, this domain will scrape traces,metrics. (default port `4317` for grpc )
- `OTEL_SERVICE_NAME`: Project name that show in monitor dashboard
- `OTEL_SERVICE_VERSION`: Project version
- `INSECURE_MODE`: Enable/Disable insecure mode for otel collector (disable TLS/SSL)
- `OTEL_TRACER_ENABLED`: If disable, monitoring will not implement.

##### Config Jeager:
- Check [Jeager Provider Config](/internal/core/monitoring/traces/provider.go) `(/internal/core/monitoring/traces/provider.go`
- Span Custom Package: [Jeager Span](/internal/core/monitoring/traces/utils/span.go) `/internal/core/monitoring/traces/utils/span.go`,
- Example usage:
for otel middleware:  🚀 🚀 🚀
```go

type OtelMiddleware struct {
	IsEnable bool
}


func (m *OtelMiddleware) OtelMiddleware() func(c *gin.Context) {
	return func(c *gin.Context) {
		ctxData := trace_utils.SpanData{
			Topic:    c.Request.RequestURI,
			Span:     nil,
			DebugKey: "",
			Ctx:      c.Request.Context(),
		}

		if m.IsEnable {
			ctxx, _span := trace_utils.NewSpanWithTopic(c.Request.Context(), c.Request.RequestURI, c.Request.RequestURI, nil)

			pathInfo := map[string]string{
				"path":   c.Request.URL.String(),
				"method": c.Request.Method,
			}
			trace_utils.ApplyAttributes(_span, pathInfo)

			ctxData = trace_utils.SpanData{
				Topic:    c.Request.RequestURI,
				Span:     _span,
				DebugKey: "middleware",
				Ctx:      ctxx,
			}
		}
		ctxValue := context.WithValue(c.Request.Context(), trace_utils.GlobalSpanKey, ctxData) //if monitoring not enable, mock data  🚀 
		c.Request = c.Request.WithContext(ctxValue)
		c.Next()
	}
}

func NewOtelMiddleware(IsEnable bool) *OtelMiddleware {
	return &OtelMiddleware{
		IsEnable: IsEnable,
	}
}
```

- Trace Span in repository layer:
```go
func (store *otpQueueStorage) CreateOtpQueue(ctx context.Context, queues *domain.OTPQueues) (*domain.OTPQueues, error) {
	queueModel := mapper.TransformToOTPQueueModel(queues)
	_,span := trace_utils.
		NewSpanWithTopic(ctx,"otpQueueStorage","CreateOtpQueue",nil)
	defer span.End()
	result := store.db.Debug().WithContext(ctx).Table(queueModel.Table()).Create(queueModel)
	if result.RowsAffected > 0 {
		return mapper.TransformToOTPQueueDomain(queueModel), nil
	}
	jsonErr := utils.PgErrorHandler(result.Error)
	return nil, errors.New(jsonErr)
}
```

- Config Tracer for gorm: (inject SQL statement for tracer): library: `github.com/uptrace/opentelemetry-go-extra/otelgorm v0.2.3`🔌
```text
db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		NamingStrategy: schema.NamingStrategy{
			SingularTable: true,
		},
		Logger:      gorm_log.Default.LogMode(gorm_log.Error),
		PrepareStmt: true,
	})

	if err != nil {
		log.WithFields(logger.Fields{
			"database":   "form-service postgres database",
			"connection": "disconnected",
			"issue":      "connection issue",
			"message":    err.Error(),
		}).Fatalln("form-service postgres db issue")
	} else {
		log.WithFields(logger.Fields{
			"database":   "form-service postgres database",
			"connection": "connected",
		}).Infof("form-service postgres db connected")
	}

	//pluginTracer for db
	err = db.Use(otelgorm.NewPlugin())
```
- Config tracer for redis:
using pkg: `github.com/redis/go-redis/extra/redisotel/v9 v9.0.5`
```text
import (
	"github.com/redis/go-redis/extra/redisotel/v9"
	"github.com/redis/go-redis/v9"
)

func TrackRedis(redisDB redis.UniversalClient) error {
	if err := redisotel.InstrumentTracing(redisDB); err != nil {
		return err
	}
	// Enable metrics instrumentation.
	if err := redisotel.InstrumentMetrics(redisDB); err != nil {
		return err
	}

	return nil
}
```

#### Wrap Them Up:  ⚒⚒⚒

🗝 Finally, Wrap them into a bundle:(including tracers & metrics)
```text
func Setup() error {
	OtelServiceName := appctx.AppCtx().Viper().Get(monitoring_port.OTEL_SERVICE_NAME)
	traces.NewTraceProvider()
	metrics.NewMetricProvider()
	_, err := setup.TrackMemStats(OtelServiceName)
	if err != nil {
		return err
	}
	return nil
}
```

🗝  And we have `CleanMonitoringResource` To close all exporter connection after server shutdown: 
```text

func CleanMonitoringResource(){
	err := traces.NewTraceProvider().CloseExporter()
	if err != nil{
		log.Fatalln("failed to close tracer: ",err)
	}
	_err := metrics.NewMetricProvider().CloseExporter()
	if _err != nil{
		log.Fatalln("failed to close metric: ",err)
	}
}
```

In main function we have :
```text
app.WebServerPort("8009").
		EnableMonitoring().
		WebServer(router.InstanceGin).
		Start()
```

Notice that `EnableMonitoring` is
In [setup http server file](/internal/infrastructure/http_server.go) `/internal/infrastructure/http_server.go`

```text
func OtelEnableTracker(viper _viper.IViper ) string {
	enableOtel := strings.ToUpper(strings.TrimSpace(viper.Get("OTEL_TRACER_ENABLED")))
	log.Info(fmt.Sprintf(http_server.OTELConfigDebugMsg, len(enableOtel), enableOtel, enableOtel == "TRUE"))
	return enableOtel
}

func (c *config) EnableMonitoring() *config {
	enableOtel := OtelEnableTracker(c.appCtx.Viper())
	if enableOtel == "TRUE" {
		c.enableMonitoring = true
		err := monitoring.Setup() // 🔗  🔗  🔗  Monitoring Setup here
		if err != nil {
			return HandleInitializeTracerError(c,err)
		}
		c.appCtx.Logger().Infof(http_server.MonitoringEnabled)
		app_states.GetAppState().EnableOtel()
		return c
	}
	traces.InitDefaultTracer()
	return c
}



func HandleInitializeTracerError(c *config,err error) *config {
	traces.InitDefaultTracer()
	c.logger.Errorf(fmt.Sprintf(http_server.ErrorTracerInitialize, err))
	c.enableMonitoring = false
	return c
}
```


for [](internal/infrastructure/router/gin/gin.go)

Use `monitoring.CleanMonitoringResource()` When server shutdown to close exporter connection...
