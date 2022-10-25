package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"

	_ "github.com/go-sql-driver/mysql"
)

type FlightData struct {
	T_arr       []float32 `t`
	A_arr       []float32 `a`
	B_arr       []float32 `b`
	Cch_arr     []int     `Cch`
	East_arr    []float32 `East`
	H_arr       []float32 `H`
	Hch_arr     []int     `Hch`
	Heading_arr []float32 `Heading`
	North_arr   []float32 `North`
	Pitch_arr   []float32 `P`
	Roll_arr    []float32 `R`
	Speed_arr   []float32 `V`
	Theta_arr   []float32 `Theta`
	Yaw_arr     []float32 `Y`
	CLch_arr    []int     `CLch`
}

type CompilerResult struct {
	Res string `res`
	Log string `log`
}

func Serve(w http.ResponseWriter, r *http.Request) {

	fmt.Println("Serving file")
	fmt.Println(r.URL.Path)

	_html := "." + r.URL.Path

	if _html == "/" {
		http.ServeFile(w, r, "./index.html")
		return
	}

	http.ServeFile(w, r, _html)

}

const one_plot_points = 100

func SQLQurey() FlightData {

	var t_arr = make([]float32, 0, one_plot_points)
	var a_arr = make([]float32, 0, one_plot_points)
	var b_arr = make([]float32, 0, one_plot_points)
	var Cch_arr = make([]int, 0, one_plot_points)
	var East_arr = make([]float32, 0, one_plot_points)
	var H_arr = make([]float32, 0, one_plot_points)
	var Hch_arr = make([]int, 0, one_plot_points)
	var Heading_arr = make([]float32, 0, one_plot_points)
	var North_arr = make([]float32, 0, one_plot_points)
	var Pitch_arr = make([]float32, 0, one_plot_points)
	var Roll_arr = make([]float32, 0, one_plot_points)
	var Speed_arr = make([]float32, 0, one_plot_points)
	var Theta_arr = make([]float32, 0, one_plot_points)
	var Yaw_arr = make([]float32, 0, one_plot_points)
	var CLch_arr = make([]int, 0, one_plot_points)

	db, err := sql.Open("mysql",
		"root:1155@tcp(localhost:3306)/plane_model_results")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	var (
		t, a, b, Cch, East, H, Hch, Heading, North, Pitch, Roll, Speed, Theta, Yaw, CLch float32
	)

	rows, err := db.Query(`call GetData()`)

	if err != nil {
		log.Fatal(err)
	}

	defer rows.Close()

	for rows.Next() {

		err := rows.Scan(&t, &a, &b, &Cch, &East, &H, &Hch, &Heading, &North, &Pitch, &Roll, &Speed, &Theta, &Yaw, &CLch)
		if err != nil {
			log.Fatal(err)
		}

		t_arr = append(t_arr, t)
		a_arr = append(a_arr, a)
		b_arr = append(b_arr, b)
		Cch_arr = append(Cch_arr, int(Cch))
		East_arr = append(East_arr, East)
		H_arr = append(H_arr, H)
		Hch_arr = append(Hch_arr, int(Hch))
		Heading_arr = append(Heading_arr, Heading)
		North_arr = append(North_arr, North)
		Pitch_arr = append(Pitch_arr, Pitch)
		Roll_arr = append(Roll_arr, Roll)
		Speed_arr = append(Speed_arr, Speed)
		Theta_arr = append(Theta_arr, Theta)
		Yaw_arr = append(Yaw_arr, Yaw)
		CLch_arr = append(CLch_arr, int(CLch))

	}
	err = rows.Err()
	if err != nil {
		log.Fatal(err)
	}

	return FlightData{T_arr: t_arr, A_arr: a_arr, B_arr: b_arr,
		Cch_arr:     Cch_arr,
		East_arr:    East_arr,
		H_arr:       H_arr,
		Hch_arr:     Hch_arr,
		Heading_arr: Heading_arr,
		North_arr:   North_arr,
		Pitch_arr:   Pitch_arr,
		Roll_arr:    Roll_arr,
		Speed_arr:   Speed_arr,
		Theta_arr:   Theta_arr,
		Yaw_arr:     Yaw_arr,
		CLch_arr:    CLch_arr}
}

func SendJson(w http.ResponseWriter, r *http.Request) {

	j, _ := json.Marshal(SQLQurey())

	w.Write([]byte(j))
}

func SendCode(w http.ResponseWriter, r *http.Request) {

	fmt.Println("Serving code")
	fmt.Println(r.URL.Path)

	http.ServeFile(w, r, "."+r.URL.Path)
}

func Compile(w http.ResponseWriter, r *http.Request) {

	fmt.Println("Compile")

	b, err := io.ReadAll(r.Body)
	// b, err := ioutil.ReadAll(resp.Body)  Go.1.15 and earlier
	if err != nil {
		log.Fatalln(err)
	}

	fmt.Println(string(b))

	f, err := os.Create("./compiler/tmp.asm")

	if err != nil {
		log.Fatal(err)
	}

	path, err := os.Getwd()
	if err != nil {
		log.Println(err)
	}

	defer f.Close()

	_, err2 := f.WriteString(string(b))

	if err2 != nil {
		log.Fatal(err2)
	}

	path = path + "\\compiler\\run.bat"

	cmd := exec.Command(path)
	cmd.Run()
	cmd.Wait()

	res, err := os.ReadFile("./compiler/results.txt")

	if err != nil {
		log.Fatal(err)
	}
	fmt.Print(string(res))

	log_, err := os.ReadFile("./compiler/log.txt")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Print(string(log_))

	toSend := CompilerResult{string(res)[0 : len(res)-48], string(log_)}

	j, _ := json.Marshal(toSend)

	w.Write([]byte(j))
}

func main() {

	http.HandleFunc("/", Serve)
	http.HandleFunc("/data", SendJson)
	http.HandleFunc("/code/", SendCode)
	http.HandleFunc("/compile", Compile)

	http.ListenAndServe(":8080", nil)

}
