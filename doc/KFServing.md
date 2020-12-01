# Kubernetes

[video link](https://www.youtube.com/watch?v=X48VuDVv0do)

## What is k8s

Open source container orchestration tool

Helps you manage containers 

Containers for micro service

Features:

1. High availability or no downtime
2. Scalability or high performance
3. Disaster recovery - backup and restore



## Component:

Pod:

1. Smallest unit of k8s
2. Abstraction over container
3. Usually 1 application per Pod
4. Each Pod gets its own IP address
5. New IP address on re-creation 

Service:

1. permanent IP address
2. lifecycle of Pod and Service NOT connected
3. External service: Open communications to the external resources. An http protocol with a node ip address (not the service) and the port number of the service
4. Internal service: Other service except External service
5. Ingress https://my-app.com instead of xx.xx.xx.xx:xxxx

ConfigMap:

1. external configuration of your application

Secret:

1. Config, but used to store secret data
2. base64 encoded

Volumes:

1. Storage on local machine or remote, outside of the k8s cluster
2. k8s doesn't manage data persistance

Service has 2 functionalities:

1. permanent IP
2. load balancer: the service will catch the request and forward it to which ever pod is busy

Deployment:

1. blueprint for my-app pods. (replica)
2. you create Deployments
3. abstraction of pods

StatefulSet: (database)

1. For stateful apps or Databased
2. Deploying Stateful not easy
3. DB are often hosted outside of k8s cluster

## Architecture explained

Worker machine in k8s cluster (node)

1. each Node has multiple Pods on it

2. 3 process muse be installed on every Node

3. Worker Nodes do the actural work

   (1) container runtime (2) Kublet (interacts with both the container and node; starts the pod with a conainer inside) (3) kube proxy (forward the request)

Masterprocess

1. 4 processes run on every master node

   (1) api server

   	1. cluster gateway
    	2. acts as a gate keeper for authentication 
    	3. some request -> API server -> validate request -> other process -> pod

   (2) Scheduler

   1. schedule new pod -> API server -> scheduler -> where to put the pod
   2. Scheduler just decide on whih node new pod should be scheduled

   (3) Controller manager

   1. detects cluster state changes
   2. Controller manager -> schedule -> kubelet

   (4) etcd

   1. etcd is the cluster brain
   2. cluster changes get stored in the key value store
   3. Application data is not stored in etcd

2. Multiple master where each masternode runs its master process. Distributed storage accross all master nodes.

## Example Cluster Set-Up

1. 2 Master Nodes    Less resources

   3 Worker Nodes.   More resoures

2. Add new Master/Node server

   (1) get new bare server

   (2) install all the master/worker node professes

   (3) add it to the cluster

## What is Minikube

Production Cluster Setup

1. Multiple master and worker nodes
2. Separate virtual or physical machines

Test on local machine -> qinikube

1. create VIrtual Box on your laptop
2. Node runs in that Virtual Box
3. 1 Node K8s cluster
4. for testing purposes

## What is kubectl

comand line tools for k8s cluster

talk to Api Server

## Basic kubectl commands

``` bash
kubectl get nodes
kubectl get pod
kubectl get services
kubectl create [name] --image=[iamgedir]
kubectl get deployment
kubectl get replicaset
kubectl edit deployment [name]
kubectl logs [podname]
kubectl describe pod [podname]
kubectl exec -it [podname] -- bin/bash
kubectl delete deployment [name]
kubectl apply -f [filename]
```

 Pod is the smallest unit, but you create deployment, which is abstraction over pods

 Replicaset is managign the replica of a pod

1. Deployment manages a replicaset
2. Replicaset manages a pod
3. Pod is an abstraction of container

## Configuration file

Each configuration file has 3 parts

1. metadata
2. specification
3. status: Etch holdes the status of all the components

Use yaml validator 

Template

1. has its own metadata and spec section
2. applies to pod
3. blueprint for a pod

connecting deployment to pods

1. pods get the label through the template blueprint

2. this label is matched by the selector

connecting services to deployment

Ports

DBservice -> port -> nginx service -> target port -> pod

Serice

1. Selector: to connect to pod through label

2. ports
   1. Port: service port
   2. containerport of deployment
3. type LoadBalancer
   1. asigns service an external IP address and so accepts external requests
4. nodePort: 
   1. port for external IP address
   2. Port you need to put into your browser
   3. 300000-32767
5. minikube service xxxxx

## Namespace

1. Organise resources in namespace
2. virtual cluster inside a cluster

## Ingress explained

routing rules: forward request to the internal service

Host;

1. valid domain address
2. map domain name to Node's IP address, which is the entrypoint

Ingress Controller:

1. evaluates all the rules
2. manages redirections
3. entrypoint to cluster
4. many third-party implementations
5. K8s nginx ingress controller

proxy server -> ingress controller

Configure ingress controller in minikube

1. install ingress controller in minikube

   ```minikube addons enable ingress```

2. create ingress rule

## Helm explained

Package Manager for Kubernetes

​	To package YAML Files and distribute them in public and private repositories

Helm Charts

1. Bundle of YAML FIles
2. Create your own Helm Charts with Helm
3. Push them to Helm Repository
4. Download and use. existing ones

## Kubenetes Volumes explained

1. storage that doesn't depend on the pod lifecycle
2. storage must be available on all nodes
3. storage needs to survie even if cluster crashes

Persistent Volume

1. a cluster resource
2. created via YAML file
   1. kind: PersistentVolume
   2. spec: e.g. how much storage?

Persistent Volume Clain

1. Use that PVC in Pods configuration 
2. Clains must be in the same namespace

ConfigMap and Secret

1. local volumes
2. not created via PV and PVC
3. managed by Kubernetes

Storage Class

​	StorageBackend is defined in the SC component

1. Via "provisioner" attribute
2. each storage backend has own provisioner
3. internal provisioner - "kubernetes.io"
4. external provisioner
5. Configure parameters for storage we want to request for PV

​     Another abstraction level

1. abstracts underlying storage provider
2. parameters for the storage

1) Pod claines storage via PVC

2) PVC requests stroage from SC

3) SC creates PV that meets the needs of the Claim

## k8s StatefulSet explained

1. example of stateful applications:
   1. databases
   2. applications that store data

2. don't keep record of state

3. each request is completely new

## k8s Service explained

Each Pod has its own IP address

1. Pods are ephemeral - are destroyed frequently

Service

1. stable IP address
2. loadbalancing
3. Loose coupling
4. Within & outside service

ClusterIP Services

1. default type
2. IP address from Node's port
3. Selector
   1. Pods are identified via selectors
   2. Key value pairs
   3. labels of pods
   4. random label names
4. k8s creates endpoint object 
   1. same name as service 
   2. keep track of, which pods are the members/endpoints of the service
5. service port is arbitrary
6. Targetport must match the port, the container is listening at

Headless Services

1. Client wants to communicate with 1 specific pod directly
2. Pods want to talk directly with specific pod
3. so, not randomly selected
4. Use case; Stateful applications, like databases
5. Pod replicas are not identical
6. DNS lookup
   1. DNS lookup for service - returns single IP address (Cluster IP)
   2. Set ClusterIP to "none" - returns Pod IP address instead

NodePort Service

1. External traffic has access to fixed port on each worker node
2. Node port range: 30000 - 32767

LoadBalancer Service

1. becomes accessible externally through cloud providers LoadBalancer
2. LoadBalancer Service is an extension of NodePort Service
3. NodePort Service is an extension of ClusterIP Service

# Istio

[video link](https://www.youtube.com/watch?v=2FyhNONICkY)

An open platform to connect, secure, control and observe services.

service mesh

custom resource definition (CRD) are a mechanism that allows you to extend kubernetes and  to add your own types in kubernetes

Virtualservice are crd by istio 

# Knative

如同许多新的概念一样，Serverless目前还没有一个普遍公认的权威的定义。最新的一个定义是这样描述的：“无服务器架构是基于互联网的系统，其中应用开发不使用常规的服务进程。相反，它们仅依赖于第三方服务（例如AWS Lambda服务），客户端逻辑和服务托管远程过程调用的组合。”

Knative 是谷歌牵头发起的 Serverless 项目，其定位为基于 Kubernetes 的 Serverless 解决方案，旨在标准化 Serverless，简化其学习成本。Knative 是以 Kubernetes 的一组自定义资源类型（CRD）的方式来安装的，因此只需使用几个 YAML 文件就可以轻松地开始使用 Knative 了。

Knative 就是基于 Kubernetes 的应用 Serverless 编排系统。实际上 Knative 包含的不单单是 Workload，它还有 Kubernetes 原生的流程编排引擎和完备的事件系统。

Knative 将重点放在两个关键组件上：为其提供流量serving（服务），以及确保应用程序能够轻松地生产和消费event（事件）。

1. Serving（服务）

   基于负载自动伸缩，包括在没有负载时缩减到零。允许你为多个修订版本（revision）应用创建流量策略，从而能够通过 URL 轻松路由到目标应用程序。

2. Event（事件）

   使得生产和消费事件变得容易。抽象出事件源，并允许操作人员使用自己选择的消息传递层。

# KFServing

KFServing provides a Kubernetes [Custom Resource Definition](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) for serving machine learning (ML) models on arbitrary frameworks.



### Kubernetes Clusters

Kubernetes coordinates a highly available cluster of computers that are connected to work as a single unit. It automates the distribution and scheduling of application containers across a cluster in a more efficient way.

A Kubernetes cluster consists of two types of resources:

1. The **Master** coordinates the cluster. The Master is responsible for managing the cluster.
2. **Nodes** are the workers that run applications. A node is a VM or a physical computer that serves as a worker machine in a Kubernetes cluster.

``` bash
# Create a Cluster
minikube start # start to run Kubernetes
kubectl version # kubectl: interacting with Kubernetes
kubectil get nodes # Show all nodes that can be used to host the applications

```

We can deploy the containerized applications on top of it. To do so, you create a Kubernetes **Deployment** configuration. It instructs Kubernetes how to create and update instances of your application.

![k8s-cluster](./pic/k8s-cluster.png)

``` bash
# common format: kubectl [action] [resource]
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1
kubectl get deployments # List the deployments
```



 A Pod is a Kubernetes abstraction that represents a group of one or more application containers (such as Docker), and some shared resources for those containers. Resources are:

1. Shared storage, as Volumes
2. Networking, as a unique cluster IP address
3. Information about how to run each container, such as the container image version or specific ports to use

A Pod always runs on a **Node**. A Node is a worker machine in Kubernetes and may be either a virtual or a physical machine, depending on the cluster.

Recall that Pods are running in an isolated, private network - so we need to proxy access to them so we can debug and interact with them. To do this, we'll use the `kubectl proxy` command to run a proxy in a second terminal window. Click on the command below to automatically open a new terminal and run the `proxy`

``` bash
kubectl get namespaces
kubectl get pods -n [namespace]
kubectl describe pods

# Let’s list the environment variables:
kubectl exec $POD_NAME env
# let’s start a bash session in the Pod’s container:
kubectl exec -ti $POD_NAME bash

# To see the ReplicaSet created by the Deployment, run
kubectl get rs
```

yaml规则

``` yam
＃ 第一段
apiVersion: vl 
kind: Pod 
metadata:
	name: <string> 
	namespace: [string] 
	labels:
		－ name: [string] 
  annotations:
		- name: [string]
＃ 第二段
spec :
	containers:
	- name: <string> 
	  image: <string> 
	  imagePullPolicy: [Always|Never|IfNotPresent]
	  command: [string] 
	  args: [string) 
	  workingDir: [string) 
	  volumeMounts:
		- name: <string> 
			mountPath: <string> 
			readOnly: [true|false)
```



### Architecture

在 Kubenetes 中， Service 是分布式集群架构的核心。 它是一种抽象的概念，每一个 Service 的后 端有多个 Pod ， 所有的容器均在 Pod 中运行。

每个 Service 拥有一个唯一指定的名字，拥有一个虚拟 IP 和相应的端口号.

Kubernetes 的 Node 节点主要由三个模块组成： kubelet 、 kube-proxy 、 runtime。

1. Kubelet。 Kubelet 是 Master 在每个 Node 节点上的 agent ，是 Node 与 Master 通信的重要途径。
2. Kube-proxy。 该模块实现了 Kubernetes 中的服务发现和反向代理功能。
3. runtimeo runtime 指的是容器运行环境，目前 Kubernetes 支持 Docker 和 Rocket



Deployment

一旦运行了 Kubernetes 集群，就可以在其上部署容器化应用程序。 为此，您需要创建 Kubernetes **Deployment** 配置。Deployment 指挥 Kubernetes 如何创建和更新应用程序的实例。

Pod

Pod 是 Kubernetes 抽象出来的，表示一组一个或多个应用程序容器（如 Docker），以及这些容器的一些共享资源。这些资源包括:

- 共享存储，当作卷
- 网络，作为唯一的集群 IP 地址
- 有关每个容器如何运行的信息，例如容器映像版本或要使用的特定端口。

Service

Kubernetes Service 定义了这样一种抽象：逻辑上的一组 Pod，一种可以访问它们的策略 —— 通常称为微服务。

Kubernetes [Pod](https://kubernetes.io/zh/docs/concepts/workloads/pods/) 是转瞬即逝的。 Pod 实际上拥有 [生命周期](https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-lifecycle/)。 当一个工作 Node 挂掉后, 在 Node 上运行的 Pod 也会消亡。 [ReplicaSet](https://kubernetes.io/zh/docs/concepts/workloads/controllers/replicaset/) 会自动地通过创建新的 Pod 驱动集群回到目标状态，以保证应用程序正常运行。

LoadBalancer

负载均衡器Load Balancer服务是NodePort服务的扩展，负载均衡器拥有独立的可公开访问的IP地址，并将所有连接都重定向到服务，外部客户端可以通过负载均衡器的IP地址访问到集群内部的服务。

helm

Package manager



### Knative & Istio

KFServing currently requires Knative Serving for auto-scaling, canary rollout, Istio for traffic routing and ingress.

Knative & Lstio are foundmental layers for serverless and networking.



Knative provides a set of building blocks that enable declarative, container-based, serverless workloads on Kubernetes. Knative Serving proves primitives for serving platforms such as:

1. Event triggered functions on Kubernetes
2. Scale to and from zero
3. Queue based autoscaling for CPUs and TPUs. KNative autocaling by default provies inflight requests per pod
4. Traditional CPU autoscaling if desired. Traditional scaling hard for disparate devices (GPU, CPU, TPU)



Istio: An open service mesh platform to connect, observe, secure and control microservices.



### Analysis

``` bash
main.go: kfserving/cmd/manager/main.go
```

1. Parser

2. Get Config [Config](https://medium.com/@onexlab.io/golang-config-file-best-practise-d27d6a97a65a) 

   ``` go
   config.GetConfig()
   ```

3. Create manager controller [manager](https://github.com/kubernetes-sigs/controller-runtime/blob/master/pkg/manager/manager.go)

   ``` go
   manager.New()
   // Manager initializes shared dependencies such as Caches and Clients, and provides them to Runnables.
   // A Manager is required to create Controllers.
   
   func New(config *rest.Config, options Options) (Manager, error)
   // New returns a new Manager for creating Controllers.
   
   mgr, err := manager.New(cfg, manager.Options{MetricsBindAddress: metricsAddr, Port: 9443})
   // cfg, err := config.GetConfig()
   // MetricsBindAddress:
   // MetricsBindAddress is the TCP address that the controller should bind to
   // for serving prometheus metrics.
   // It can be set to "0" to disable the metrics serving.
   ```

4. Setup controllers

   problem: [link](k8s.io/client-go/tools/record) 404 for func ```eventBroadcaster := record.NewBroadcaster()```

   

5. Creates a new Clientset for the given config.

​	  [link](https://godoc.org/k8s.io/client-go/kubernetes#NewForConfig)  func  ``` kubernetes.NewForConfig(mgr.GetConfig())```

​	``` func NewForConfig(c *rest.Config) (*Clientset, error)```

6. Setup trainedmodel controller

``` trainedModelEventBroadcaster := record.NewBroadcaster()```

7. Get web hook server

``` go
hookServer.Register("/mutate-pods", &webhook.Admission{Handler: &pod.Mutator{}})

func (s *Server) Register(path string, hook http.Handler)
// Register marks the given webhook as being served at the given path.
// It panics if two hooks are registered on the same path.
```

Controller logic in ```kfserving/pkg/controller```



``` go
// Parser
// Get Config
// Create manager controller
// Creates a new event broadcaster.
// Creates a new Clientset for the given config.
// Setup controllers
// Setup trainedmodel controller
// Get webhook server


package main

import (
	"flag"
	"sigs.k8s.io/controller-runtime/pkg/client/config"
	"sigs.k8s.io/controller-runtime/pkg/manager"
	"k8s.io/client-go/tools/record"
	"k8s.io/client-go/kubernetes"
	typedcorev1 "k8s.io/client-go/kubernetes/typed/core/v1"


)

func main() {
	var flagAddr string
	flag.StringVar(&flagAddr, "Address", ":8080", "The address the metric endpoint binds to.")
	flag.Parse()

	// GetConfig creates a *rest.Config for talking to a Kubernetes API server. If --kubeconfig 
	// is set, will use the kubeconfig file at that location. Otherwise will assume running in 
	// cluster and use the cluster provided kubeconfig.
	cfg, err := config.GetConfig()

	// New returns a new Manager for creating Controllers.
	mng, err := manager.New(cfg, manager.Options(MetricsBindAddress: flagAddr, Port: 9443))

	// Creates a new event broadcaster.
	eventBroadcaster = record.NewBroadcaster()

	// NewForConfig creates a new Clientset for the given config. If config's RateLimiter is not 
	// set and QPS and Burst are acceptable, NewForConfig will generate a rate-limiter in configShallowCopy.
	clentSet, err := kubenetes.NewForConfig(mng.GetConfig())

	// EventSink knows how to store events (client.Client implements it.)
	// EventSink must respect the namespace that will be embedded in 'event'.
	// It is assumed that EventSink will return the same sorts of errors as
	// func (c *CoreV1Client) Events(namespace string) EventInterface
	eventSink := &typedcorev1.EventSinkImpl{Interface: clientSet.CoreV1().Events("")}
	// StartRecordingToSink starts sending events received from this EventBroadcaster to the given
	// sink. The return value can be ignored or used to stop recording, if desired.
	eventBroadcaster.StartRecordingToSink(eventSink)

	trainedModelEventBroadcaster = record.NewBroadcaster()

	eventSink := &typedcorev1.EventSinkImpl{Interface: clientSet.CoreV1().Events("")}
	trainedModelEventBroadcaster.StartRecordingToSink(eventSink)

	// GetWebhookServer returns a webhook.Server
	server := mng.GetWebhookServer()
	// Register marks the given webhook as being served at the given path. It panics if two hooks are 
	// registered on the same path.
	server.register()

}
```



Controller: 在K8S 拥有很多controller 他们的职责是保证集群中各种资源的状态和用户定义(yaml)的状态一致, 如果出现偏差, 则修正资源的状态.

Controller manager: controller manager 是各种controller的管理者,是集群内部的管理控制中心.

Event: 它存储在Etcd里，记录了集群运行所遇到的各种大事件。

Webhook: WebHook 是一种 HTTP 回调：某些条件下触发的 HTTP POST 请求；通过 HTTP POST 发送的简单事件通知。一个基于 web 应用实现的 WebHook 会在特定事件发生时把消息发送给特定的 URL. 具体来说，当在判断用户权限时，`Webhook` 模式会使 Kubernetes 查询外部的 REST 服务。



### client-go

``` go
import "k8s.io/client-go/kubernetes"
```

RESTClient: Uniform Interface The uniform interface constraint defines the interface between clients and servers.



```
--| pkg
--| --| controller
--| --| --| v1alpha2
--| --| --| --| inferenceservice
--| --| --| --| --| reconcilers
--| --| --| --| --| --| istio
--| --| --| --| --| --| --| virtualservice_reconciler.go
--| --| --| --| --| --| knative
```

``` 
1. 
controller/v1alpha2/inferenceservice/controller.go

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
	
2. 
controller/v1alpha2/inferenceservice/reconcilers/knative/service_reconciler.go

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
	本质上就是把desired 赋值赋给existing
	
func semanticEquals:
	deepequal of two service
	
3. controller/v1alpha2/inferenceservice/reconcilers/istio/virtualservice_reconciler.go

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
	
4. 	
controller/v1beta1/inferenceservice/controller.go

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



[https://pkg.go.dev/github.com/kubeflow/kfserving/pkg/apis/serving/v1alpha2#InferenceService](https://pkg.go.dev/github.com/kubeflow/kfserving/pkg/apis/serving/v1alpha2#InferenceService)

Inference service

pkg/apis/serving/v1alpha2/inferenceservice_types.go

All the specs are in this file

```go
type InferenceService struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   InferenceServiceSpec   `json:"spec,omitempty"`
	Status InferenceServiceStatus `json:"status,omitempty"`
}

// TypeMeta describes an individual object in an API response or request with strings representing the type of the object and its API schema version. Structures that are versioned or persisted should inline TypeMeta.
type TypeMeta struct {
	// Kind is a string value representing the REST resource this object represents.
	// Servers may infer this from the endpoint the client submits requests to.
	// Cannot be updated.
	// In CamelCase.
	// More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
	// +optional
	Kind string `json:"kind,omitempty" protobuf:"bytes,1,opt,name=kind"`

	// APIVersion defines the versioned schema of this representation of an object.
	// Servers should convert recognized schemas to the latest internal value, and
	// may reject unrecognized values.
	// More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
	// +optional
	APIVersion string `json:"apiVersion,omitempty" protobuf:"bytes,2,opt,name=apiVersion"`
}


```





[knative.dev/serving/pkg/apis/serving/v1](https://godoc.org/knative.dev/serving/pkg/apis/serving/v1)

```go
knative.dev/serving/pkg/apis/serving/v1

type Service struct {
    metav1.TypeMeta `json:",inline"`
    // +optional
    metav1.ObjectMeta `json:"metadata,omitempty"`

    // +optional
    Spec ServiceSpec `json:"spec,omitempty"`

    // +optional
    Status ServiceStatus `json:"status,omitempty"`
}
```



Explainer: a model explanation server

Transformer: transformer service for pre/post processing

pkg/constants/constants.go

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



```
pkg/apis/serving/v1alpha2/explainer.go

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



Question:  Corev1, knservingv1 Service difference





Run in ONNX runtime

kfserving/config/configmap/inferenceservice.yaml

``` go
"onnx": {
  "image": "mcr.microsoft.com/onnxruntime/server",
  "defaultImageVersion": "v1.0.0",
  "supportedFrameworks": [
    "onnx"
  ],
  "multiModelServer": "false"
},
```



kfserving/pkg/apis/serving/v1alpha2/framework_onnx_test.go

kfserving/pkg/apis/serving/v1alpha2/framework_onnx.go









How to start with tensorflow:

``` go
func (t *TensorflowSpec) GetContainer(modelName string, parallelism int, config *InferenceServicesConfig) *v1.Container
```



```kfserving/pkg/apis/serving/v1alpha2/predictor.go```

``` go
func getPredictor(predictorSpec *PredictorSpec) (Predictor, error) {
	predictors := []Predictor{}
	if predictorSpec.Custom != nil {
		predictors = append(predictors, predictorSpec.Custom)
	}
	if predictorSpec.XGBoost != nil {
		predictors = append(predictors, predictorSpec.XGBoost)
	}
	if predictorSpec.SKLearn != nil {
		predictors = append(predictors, predictorSpec.SKLearn)
	}
	if predictorSpec.Tensorflow != nil {
		predictors = append(predictors, predictorSpec.Tensorflow)
	}
	if predictorSpec.ONNX != nil {
		predictors = append(predictors, predictorSpec.ONNX)
	}
	if predictorSpec.PyTorch != nil {
		predictors = append(predictors, predictorSpec.PyTorch)
	}
	if predictorSpec.Triton != nil {
		predictors = append(predictors, predictorSpec.Triton)
	}
	if len(predictors) != 1 {
		err := fmt.Errorf(ExactlyOnePredictorViolatedError)
		klog.Error(err)
		return nil, err
	}
	return predictors[0], nil
}
```





https://blog.csdn.net/luanpeng825485697/article/details/106986791/

kfserving 内部使用的是knative。

封装了一层InferenceService的k8s自定义资源，来实现knative中serving的services,route,configurations,revision



Q: 您好，请问KFserving是如何将模型打包成容器部署到节点的呢？整个流程是咋样的？

A: 模型存储在pv里面，容器只是环境，将模型地址传递给kfserving的容器，容器启动就能提供服务化



CRD:

use the MultiNamespacedCacheBuilder to watch a specific set of namespaces

use the `omitempty` struct tag to mark that a field should be omitted from serialization when empty

```
go mod init elastic-serving
kubebuilder init --domain example.com
kubebuilder create api --group batch --version v1 --kind CronJob

```

The [context](https://golang.org/pkg/context/) is used to allow cancelation of requests, and potentially things like tracing. It’s the first argument to all client methods. The `Background` context is just a basic context without any extra data or timing restrictions.