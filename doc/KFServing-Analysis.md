```kfserving/cmd/manager/main.go```

``` go
Parser
Get Config
Create manager controller
Creates a new event broadcaster.
Creates a new Clientset for the given config.
Setup controllers
Setup trainedmodel controller
Get webhook server
```

Packages required:

1. k8s related
2. kfsercing v1alpha2, v1beta1 (including inferenceservice & trainedmodel), webhook, servingv1



V1alpha2 has inference service and V1beta1 has inference service and trained model

``` kfsercing/controller/v1alpha2/inferenceservice/controller.go```

``` go
func Reconcile:
  get inference service
  get config
  reconcilers using knative.NewServiceReconciler and istio.NewVirtualServiceReconciler
  update service status

func InferenceServiceReadiness:
	return if ready
	
func updateStatus:
	get existing inference service
	get namespace
	get if existing is ready
	check if existing is equal to desired
	get if desired is ready
	if desired not ready && existing ready, move to unready
	else if desired ready && existing ready, move to ready
```



```kfserving/controller/v1beta1/inferenceservice/controller.go```

``` go
func Reconcile:
	get v1beta1api inference service
	get new service config
	reconcilers using newpredictor
	if transformer is not none, append it
	if expaliner is not none, append it
	get ingressconfig
	get infressreconciler
	update serice status
```

Packages required:

1. k8s related
2. pkg/apis, pkg/constants, istio, knative

pkg/constants store all the constants including some ports and arguments

Example

``` go
// InferenceService Component enums
const (
	Predictor   InferenceServiceComponent = "predictor"
	Explainer   InferenceServiceComponent = "explainer"
	Transformer InferenceServiceComponent = "transformer"
)

// InferenceService verb enums
const (
	Predict InferenceServiceVerb = "predict"
	Explain InferenceServiceVerb = "explain"
)
```



```controller/v1alpha2/inferenceservice/reconcilers/knative/service_reconciler.go```

``` go
func NewServiceReconciler:
	create servcereconciler
	
func Reconcile:
	with predictor transformer & explainer (in constants.go)
	loop reconciler inferenceservice component with canery false
	loop reconciler inferenceservice component with canery true
	
func reconcileComponent:
	get endpointSpec
	get servicename
	create inferene service component
	if created is nil finalize Service and propagate status
	else reconcile service and propagate status
	
func finalizeService:
	get existing service
	delete it

func reconcileService:
	get existing service
	return if no differences to reconcile
	get diff from desired.Spec.ConfigurationSpec and existing.Spec.ConfigurationSpec
	desired configuration Spec and ObjectMeta labels -> existing
	
func semanticEquals:
	deepequal of two service
```

packages required

1. k8s

2. pkg/kmp

3. resources/knative

   

``` controller/v1alpha2/inferenceservice/reconcilers/istio/virtualservice_reconciler.go```

``` go
func NewVirtualServiceReconciler
	create virtual service reconciler
	
func Reconcile:
	create virtual service -> desired
	reconcileExternalService inference service
	reconcileVirtualService with desired
	propagate route status
	
func reconcileExternalService:
	desired = corev1.Service{with spec}
	existing = corev1.Service
	check if equal
	get dif from two spec
	existing.Spec = desired.Spec
	existing.ObjectMeta.Labels = desired.ObjectMeta.Labels
	existing.ObjectMeta.Annotations = desired.ObjectMeta.Annotations
	update
	
func reconcileVirtualService:
	existing = virtualservice
	check if equal
	get diff from two spec
	existing.Spec = desired.Spec
	existing.ObjectMeta.Labels = desired.ObjectMeta.Labels
	existing.ObjectMeta.Annotations = desired.ObjectMeta.Annotations
	update
```

Packages required:

1. k8s
2. Istio.io
3. resources/istio
4. pkg/kmp
5. apis/servng



``` apis/serving/v1alpha2/inferenceservice_types.go``` : All the specs are in this file including 

``` go
type InferenceService struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   InferenceServiceSpec   `json:"spec,omitempty"`
	Status InferenceServiceStatus `json:"status,omitempty"`
}
```

and a lot of apis' spec



Explainer: a model explanation server

Transformer: transformer service for pre/post processing

Predictor: prediction

```pkg/apis/serving/v1alpha2/explainer.go```

``` go
func GetStorageUri
	getExplainer
	get storage URI from explainer
	
func CreateExplainerContainer
	getExplainer
	create explainer container
	
func ApplyDefaults
	getExplainer
	apply defaults config
	
func Validate
	get explainer
	validate
	
func getExplainer
	handlers is an array of Explainer
	try append explainerSpec.Custom
	try append explainerSpec.Alii
	try append explainerSpec.AIX
	if append only one of them, then correct and return
```



