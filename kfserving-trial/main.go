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