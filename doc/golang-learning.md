# Golang-learning

## 基础指令

```go
go run xxx.go
go mod init xxx
go build // make Go locate the module and add it as a dependency to the go.mod file.
go test
```

`go run` command is a useful shortcut for compiling and running a single-file program



加代理

```go env -w GOPROXY=https://goproxy.cn```

基本语法

1. `:=` operator is a shortcut for declaring and initializing a variable in one line

```go
message := fmt.Sprintf("Hi, %v. Welcome!", name)
```

```go
var message string
message = fmt.Sprintf("Hi, %v. Welcome!", name)
```

是等价的

2. 单独的数据类型 ```error```

   return nil 代表没有错误

