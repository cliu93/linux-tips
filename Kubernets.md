# Kubernets learning notes

## Kubectl common commands:
```bash
# Check kubectl version
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"15", GitVersion:"v1.15.0", GitCommit:"e8462b5b5dc2584fdcd18e6bcfe9f1e4d970a529", GitTreeState:"clean", BuildDate:"2019-06-19T16:40:16Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"15", GitVersion:"v1.15.0", GitCommit:"e8462b5b5dc2584fdcd18e6bcfe9f1e4d970a529", GitTreeState:"clean", BuildDate:"2019-06-19T16:32:14Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}

# View the cluster details
$ kubectl cluster-info
Kubernetes master is running at https://172.17.0.13:8443
KubeDNS is running at https://172.17.0.13:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

# View the nodes in the cluster
$ kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
minikube   Ready    master   32s   v1.15.0

# Deploy app
$ kubectl run kubernets-bootcamp --image=gcr.io/google-samples/kubernets-bootcamp:v1 --port 8080
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
deployment.apps/kubernets-bootcamp created

# List deployments
$ kubectl get deployments
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
kubernets-bootcamp   0/1     1            0           46s

# Start proxy
$ kubectl proxy

# Look for existing Pods
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
kubernetes-bootcamp-5b48cfdcbd-w4nzv   1/1     Running   0          11s

# view what containers are inside that Pod and what images are used to build those containers
$ kubectl describe pods
Name:           kubernetes-bootcamp-5b48cfdcbd-w4nzv
Namespace:      default
Priority:       0
Node:           minikube/172.17.0.9
Start Time:     Fri, 26 Jul 2019 03:06:33 +0000
Labels:         pod-template-hash=5b48cfdcbd
                run=kubernetes-bootcamp
Annotations:    <none>
Status:         Running
IP:             172.18.0.4
Controlled By:  ReplicaSet/kubernetes-bootcamp-5b48cfdcbd
Containers:
  kubernetes-bootcamp:
    Container ID:   docker://2febcd52e69802d548267a2cc2d657ce10ff0bd6d0f9c5d06111f86aad5165bd
    Image:          gcr.io/google-samples/kubernetes-bootcamp:v1
    Image ID:       docker-pullable://jocatalin/kubernetes-bootcamp@sha256:0d6b8ee63bb57c5f5b6156f446b3bc3b3c143d233037f3a2f00e279c8fcc64af
    Port:           8080/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Fri, 26 Jul 2019 03:06:35 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-d7pvd (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  default-token-d7pvd:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-d7pvd
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  28s (x2 over 28s)  default-scheduler  0/1 nodes are available: 1 node(s) had taints that the pod didn't tolerate.
  Normal   Scheduled         26s                default-scheduler  Successfully assigned default/kubernetes-bootcamp-5b48cfdcbd-w4nzvto minikube
  Normal   Pulled            24s                kubelet, minikube  Container image "gcr.io/google-samples/kubernetes-bootcamp:v1" already present on machine
  Normal   Created           24s                kubelet, minikube  Created container kubernetes-bootcamp
  Normal   Started           24s                kubelet, minikube  Started container kubernetes-bootcamp



```
