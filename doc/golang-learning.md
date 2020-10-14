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

   ``` go
   message := fmt.Sprintf("Hi, %v. Welcome!", name)
   ```

   ``` go
   var message string
   message = fmt.Sprintf("Hi, %v. Welcome!", name)
   ```

   是等价的

2. 赋值:

   ``` go
   var i, j int = 1, 2
   var c, python, java = true, false, "no!"
   ```

   ``` go
   k := 3
   c, python, java := true, false, "no!"
   ```

   ```:=``` 只可以在函数内使用

   ``` go
   const Pi = 3.14
   ```

   

   常量不能用 `:=` 语法声明。

3. 单独的数据类型 ```error```

   return nil 代表没有错误

4. for

   ``` go
   	sum := 0
   	for i := 0; i < 10; i++ {
   		sum += i
   	}
   ```

5. "while"

   ```go
   for sum < 1000 {
     sum += sum
   }
   ```
   C 中的 "while" 在go中也是for

6. 无限循环

   ``` go
   for {
   }
   ```

7. if`

   ``` go
   if x < 0 {
     return sqrt(-x) + "i"
   }
   ```

   

8. switch

   ``` go
   switch os := runtime.GOOS; os {
   	case "darwin":
   		fmt.Println("OS X.")
   	case "linux":
   		fmt.Println("Linux.")
   	default:
   		// freebsd, openbsd,
   		// plan9, windows...
   		fmt.Printf("%s.\n", os)
   	}
   ```

   

   Go 只运行选定的 case，而非之后所有的 case。 实际上，Go 自动提供了在这些语言中每个 case 后面所需的 `break` 语句。 除非以 `fallthrough` 语句结束，否则分支会自动终止。

9. 结构体

   ``` go
   type Vertex struct {
   	X int
   	Y int
   }
   
   func main() {
   	fmt.Println(Vertex{1, 2})
   }
   ```

   

   结构体字段可以通过结构体指针来访问.

   ``` go
   func main() {
   	v := Vertex{1, 2}
   	p := &v
   	p.X = 1e9
   	fmt.Println(v)
   }
   ```

   ``` go
   type Vertex struct {
   	X, Y int
   }
   
   var (
   	v1 = Vertex{1, 2}  // 创建一个 Vertex 类型的结构体
   	v2 = Vertex{X: 1}  // Y:0 被隐式地赋予
   	v3 = Vertex{}      // X:0 Y:0
   	p  = &Vertex{1, 2} // 创建一个 *Vertex 类型的结构体（指针）
   )
   
   func main() {
   	fmt.Println(v1, p, v2, v3)
   }
   ```

   ``` go
   board := [][]string{
     []string{"_", "_", "_"},
     []string{"_", "_", "_"},
     []string{"_", "_", "_"},
   }
   ```

   

10. 数组

    ``` go
    var a [2]string
    a[0] = "Hello"
    a[1] = "World"
    
    primes := [6]int{2, 3, 5, 7, 11, 13}
    ```

    

11. 切片

    ```go
    func main() {
    	primes := [6]int{2, 3, 5, 7, 11, 13}
    
    	var s []int = primes[1:4]
    	fmt.Println(s)
    }
    ```

    切片并不存储任何数据，它只是描述了底层数组中的一段。

    更改切片的元素会修改其底层数组中对应的元素。

    与它共享底层数组的切片都会观测到这些修改。

    ``` go
    q := []int{2, 3, 5, 7, 11, 13}
    r := []bool{true, false, true, true, false, true}
    s := []struct {
    		i int
    		b bool
    	}{
    		{2, true},
    		{3, false},
    		{5, true},
    		{7, true},
    		{11, false},
    		{13, true},
    	}
    ```

    ``` go
    a[0:10]
    a[:10]
    a[0:]
    a[:]
    ```

    切片拥有 **长度** 和 **容量**。

    切片的长度就是它所包含的元素个数。

    切片的容量是从它的第一个元素开始数，到其底层数组元素末尾的个数。

    切片 `s` 的长度和容量可通过表达式 `len(s)` 和 `cap(s)` 来获取。

    用 make 创建切片：

    ``` go
    a := make([]int, 5)  // len(a)=5
    
    b := make([]int, 0, 5) // len(b)=0, cap(b)=5
    
    b = b[:cap(b)] // len(b)=5, cap(b)=5
    b = b[1:]      // len(b)=4, cap(b)=4
    ```

    切片追加元素：

    ``` go
    var s []int
    printSlice(s)
    
    // 添加一个空切片
    s = append(s, 0)
    printSlice(s)
    ```

12. range

    ``` go
    var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}
    
    func main() {
      for i, v := range pow {
        fmt.Printf("2**%d = %d\n", i, v)
      }
    }
    ```

    output is 

    ``` go
    2**0 = 1
    2**1 = 2
    2**2 = 4
    2**3 = 8
    2**4 = 16
    2**5 = 32
    2**6 = 64
    2**7 = 128
    ```

    `for` 循环的 `range` 形式可遍历切片或映射。

    当使用 `for` 循环遍历切片时，每次迭代都会返回两个值。第一个值为当前元素的下标，第二个值为该下标所对应元素的一份副本。

13. 映射

    ``` go
    type Vertex struct {
    	Lat, Long float64
    }
    
    var m map[string]Vertex
    
    func main() {
    	m = make(map[string]Vertex)
    	m["Bell Labs"] = Vertex{
    		40.68433, -74.39967,
    	}
    	fmt.Println(m["Bell Labs"])
    }
    ```

    ``` go
    type Vertex struct {
    	Lat, Long float64
    }
    
    var m = map[string]Vertex{
    	"Bell Labs": Vertex{
    		40.68433, -74.39967,
    	},
    	"Google": Vertex{
    		37.42202, -122.08408,
    	},
    }
    ```

    ``` go
    type Vertex struct {
    	Lat, Long float64
    }
    
    var m = map[string]Vertex{
    	"Bell Labs": {40.68433, -74.39967},
    	"Google":    {37.42202, -122.08408},
    }
    ```

    在映射 `m` 中插入或修改元素：

    ```go
    m[key] = elem
    ```

    获取元素：

    ```go
    elem = m[key]
    ```

    删除元素：

    ```go
    delete(m, key)
    ```

    通过双赋值检测某个键是否存在：

    ```go
    elem, ok = m[key]
    ```

14. 函数值

    ``` go
    func compute(fn func(float64, float64) float64) float64 {
    	return fn(3, 4)
    }
    
    func main() {
    	hypot := func(x, y float64) float64 {
    		return math.Sqrt(x*x + y*y)
    	}
    	fmt.Println(hypot(5, 12))
    
    	fmt.Println(compute(hypot))
    	fmt.Println(compute(math.Pow))
    }
    ```

15. 函数的闭包

    Go 函数可以是一个闭包。闭包是一个函数值，它引用了其函数体之外的变量。该函数可以访问并赋予其引用的变量的值，换句话说，该函数被这些变量“绑定”在一起。

    例如，函数 `adder` 返回一个闭包。每个闭包都被绑定在其各自的 `sum` 变量上。

    ``` go
    package main
    
    import "fmt"
    
    func adder() func(int) int {
    	sum := 0
    	return func(x int) int {
    		sum += x
    		return sum
    	}
    }
    
    func main() {
    	pos, neg := adder(), adder()
    	for i := 0; i < 10; i++ {
    		fmt.Println(
    			pos(i),
    			neg(-2*i),
    		)
    	}
    }
    ```

    

    第二次调用的时候，因为adder只调用了一次，所以sum可以依旧保持原有的值。

16. 方法

    ``` go
    type Vertex struct {
    	X, Y float64
    }
    
    func (v Vertex) Abs() float64 {
    	return math.Sqrt(v.X*v.X + v.Y*v.Y)
    }
    
    func main() {
    	v := Vertex{3, 4}
    	fmt.Println(v.Abs())
    }
    ```

    Func 后面，跟着类

    ``` go
    type MyFloat float64
    
    func (f MyFloat) Abs() float64 {
    	if f < 0 {
    		return float64(-f)
    	}
    	return float64(f)
    }
    
    func main() {
    	f := MyFloat(-math.Sqrt2)
    	fmt.Println(f.Abs())
    }
    ```

    ``` go
    type Vertex struct {
    	X, Y float64
    }
    
    func (v Vertex) Abs() float64 {
    	return math.Sqrt(v.X*v.X + v.Y*v.Y)
    }
    
    func (v *Vertex) Scale(f float64) {
    	v.X = v.X * f
    	v.Y = v.Y * f
    }
    
    func main() {
    	v := Vertex{3, 4}
    	v.Scale(10)
    	fmt.Println(v.Abs())
    }
    ```

17. 指针与重定向

    ``` go
    var v Vertex
    fmt.Println(AbsFunc(v))  // OK
    fmt.Println(AbsFunc(&v)) // 编译错误！
    
    var v Vertex
    fmt.Println(v.Abs()) // OK
    p := &v
    fmt.Println(p.Abs()) // OK
    ```

18. 借口与隐式实现

    ``` go
    type I interface {
    	M()
    }
    
    type T struct {
    	S string
    }
    
    // 此方法表示类型 T 实现了接口 I，但我们无需显式声明此事。
    func (t T) M() {
    	fmt.Println(t.S)
    }
    
    func main() {
    	var i I = T{"hello"}
    	i.M()
    }
    ```

    ``` go
    type I interface {
    	M()
    }
    
    type T struct {
    	S string
    }
    
    func (t *T) M() {
    	fmt.Println(t.S)
    }
    
    type F float64
    
    func (f F) M() {
    	fmt.Println(f)
    }
    
    func main() {
    	var i I
    
    	i = &T{"Hello"}
    	describe(i)
    	i.M()
    
    	i = F(math.Pi)
    	describe(i)
    	i.M()
    }
    
    func describe(i I) {
    	fmt.Printf("(%v, %T)\n", i, i)
    }
    ```

    output is 

    ```
    (&{Hello}, *main.T)
    Hello
    (3.141592653589793, main.F)
    3.141592653589793
    ```

    

19. 空接口

    ```go
    func main() {
    	var i interface{}
    	describe(i)
    
    	i = 42
    	describe(i)
    
    	i = "hello"
    	describe(i)
    }
    
    func describe(i interface{}) {
    	fmt.Printf("(%v, %T)\n", i, i)
    }
    ```

    空接口可保存任何类型的值。（因为每个类型都至少实现了零个方法。）

20. 类型选择

    ``` go
    func do(i interface{}) {
    	switch v := i.(type) {
    	case int:
    		fmt.Printf("Twice %v is %v\n", v, v*2)
    	case string:
    		fmt.Printf("%q is %v bytes long\n", v, len(v))
    	default:
    		fmt.Printf("I don't know about type %T!\n", v)
    	}
    }
    
    func main() {
    	do(21)
    	do("hello")
    	do(true)
    }
    ```

    ``` go
    switch v := i.(type) {
    case T:
        // v 的类型为 T
    case S:
        // v 的类型为 S
    default:
        // 没有匹配，v 与 i 的类型相同
    }
    ```

21. Stringer

    ``` go
    type Person struct {
    	Name string
    	Age  int
    }
    
    func (p Person) String() string {
    	return fmt.Sprintf("%v (%v years)", p.Name, p.Age)
    }
    
    func main() {
    	a := Person{"Arthur Dent", 42}
    	z := Person{"Zaphod Beeblebrox", 9001}
    	fmt.Println(a, z)
    }
    ```

    output is 

    ```
    Arthur Dent (42 years) Zaphod Beeblebrox (9001 years)
    ```

    

    `Stringer` 是一个可以用字符串描述自己的类型。`fmt` 包（还有很多包）都通过此接口来打印值。

22. 错误

    ``` go
    import (
    	"fmt"
    	"time"
    )
    
    type MyError struct {
    	When time.Time
    	What string
    }
    
    func (e *MyError) Error() string {
    	return fmt.Sprintf("at %v, %s",
    		e.When, e.What)
    }
    
    func run() error {
    	return &MyError{
    		time.Now(),
    		"it didn't work",
    	}
    }
    
    func main() {
    	if err := run(); err != nil {
    		fmt.Println(err)
    	}
    }
    ```

23. Reader

    ``` go
    func main() {
    	r := strings.NewReader("Hello, Reader!")
    
    	b := make([]byte, 8)
    	for {
    		n, err := r.Read(b)
    		fmt.Printf("n = %v err = %v b = %v\n", n, err, b)
    		fmt.Printf("b[:n] = %q\n", b[:n])
    		if err == io.EOF {
    			break
    		}
    	}
    }
    ```

    output is 

    ```
    n = 8 err = <nil> b = [72 101 108 108 111 44 32 82]
    b[:n] = "Hello, R"
    n = 6 err = <nil> b = [101 97 100 101 114 33 32 82]
    b[:n] = "eader!"
    n = 0 err = EOF b = [101 97 100 101 114 33 32 82]
    b[:n] = ""
    ```

    ???

24. Image

25. Go 程

    Go 程（goroutine）是由 Go 运行时管理的轻量级线程。

    ```
    go f(x, y, z)
    ```

    会启动一个新的 Go 程并执行

    ```
    f(x, y, z)
    ```

    `f`, `x`, `y` 和 `z` 的求值发生在当前的 Go 程中，而 `f` 的执行发生在新的 Go 程中。

26. 信道

    信道是带有类型的管道，你可以通过它用信道操作符 `<-` 来发送或者接收值。

    ```
    ch <- v    // 将 v 发送至信道 ch。
    v := <-ch  // 从 ch 接收值并赋予 v。
    ```

    （“箭头”就是数据流的方向。）

    和映射与切片一样，信道在使用前必须创建：

    ```
    ch := make(chan int)
    ```

    默认情况下，发送和接收操作在另一端准备好之前都会阻塞。这使得 Go 程可以在没有显式的锁或竞态变量的情况下进行同步。

    ``` go
    
    func sum(s []int, c chan int) {
    	sum := 0
    	for _, v := range s {
    		sum += v
    	}
    	c <- sum // 将和送入 c
    }
    
    func main() {
    	s := []int{7, 2, 8, -9, 4, 0}
    
    
    c := make(chan int)
    go sum(s[:len(s)/2], c)
    go sum(s[len(s)/2:], c)
    x, y := <-c, <-c // 从 c 中接收
    
    fmt.Println(x, y, x+y)
    }
    ```

    

    带缓冲的信道

    信道可以是 *带缓冲的*。将缓冲长度作为第二个参数提供给 `make` 来初始化一个带缓冲的信道：

    ```
    ch := make(chan int, 100)
    ```

    仅当信道的缓冲区填满后，向其发送数据时才会阻塞。当缓冲区为空时，接受方会阻塞。

    ???

27. range 和 close

    发送者可通过 `close` 关闭一个信道来表示没有需要发送的值了。接收者可以通过为接收表达式分配第二个参数来测试信道是否被关闭：若没有值可以接收且信道已被关闭，那么在执行完

    ```
    v, ok := <-ch
    ```

    之后 `ok` 会被设置为 `false`。

    循环 `for i := range c` 会不断从信道接收值，直到它被关闭。

    *注意：* 只有发送者才能关闭信道，而接收者不能。向一个已经关闭的信道发送数据会引发程序恐慌（panic）。

    *还要注意：* 信道与文件不同，通常情况下无需关闭它们。只有在必须告诉接收者不再有需要发送的值时才有必要关闭，例如终止一个 `range` 循环。

    ``` go
    func fibonacci(n int, c chan int) {
    	x, y := 0, 1
    	for i := 0; i < n; i++ {
    		c <- x
    		x, y = y, x+y
    	}
    	close(c)
    }
    
    func main() {
    	c := make(chan int, 10)
    	go fibonacci(cap(c), c)
    	for i := range c {
    		fmt.Println(i)
    	}
    }
    ```

28. select语句

    `select` 语句使一个 Go 程可以等待多个通信操作。

    `select` 会阻塞到某个分支可以继续执行为止，这时就会执行该分支。当多个分支都准备好时会随机选择一个执行。

    ``` go
    func fibonacci(c, quit chan int) {
    	x, y := 0, 1
    	for {
    		select {
    		case c <- x:
    			x, y = y, x+y
    		case <-quit:
    			fmt.Println("quit")
    			return
    		}
    	}
    }
    
    func main() {
    	c := make(chan int)
    	quit := make(chan int)
    	go func() {
    		for i := 0; i < 10; i++ {
    			fmt.Println(<-c)
    		}
    		quit <- 0
    	}()
    	fibonacci(c, quit)
    }
    ```

29. sync.Mutex

    这里涉及的概念叫做 *互斥（mutual*exclusion）* ，我们通常使用 *互斥锁（Mutex）* 这一数据结构来提供这种机制。

    Go 标准库中提供了 [`sync.Mutex`](https://go-zh.org/pkg/sync/#Mutex) 互斥锁类型及其两个方法：

    - `Lock`
    - `Unlock`

    我们可以通过在代码前调用 `Lock` 方法，在代码后调用 `Unlock` 方法来保证一段代码的互斥执行。参见 `Inc` 方法。

    ``` go
    import (
    	"fmt"
    	"sync"
    	"time"
    )
    
    // SafeCounter 的并发使用是安全的。
    type SafeCounter struct {
    	v   map[string]int
    	mux sync.Mutex
    }
    
    // Inc 增加给定 key 的计数器的值。
    func (c *SafeCounter) Inc(key string) {
    	c.mux.Lock()
    	// Lock 之后同一时刻只有一个 goroutine 能访问 c.v
    	c.v[key]++
    	c.mux.Unlock()
    }
    
    // Value 返回给定 key 的计数器的当前值。
    func (c *SafeCounter) Value(key string) int {
    	c.mux.Lock()
    	// Lock 之后同一时刻只有一个 goroutine 能访问 c.v
    	defer c.mux.Unlock()
    	return c.v[key]
    }
    ```

    

