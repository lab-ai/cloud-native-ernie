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