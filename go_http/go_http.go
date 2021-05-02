package main

import "C"

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"time"
)

type mResponse struct {
	Body string
	StatusCode int
	Seq int
}
var client  = &http.Client{Timeout: 10*time.Second}

const URL_ENDPOINT = "https://postman-echo.com/post"
func makePostReq(seq int, url string, payload string, hKeys []string, hValues []string, chnl chan mResponse) {

	responseBody := bytes.NewBufferString(payload)
	req, err := http.NewRequest("POST", url, responseBody)
	if err != nil {
		fmt.Println("Invalid Post Request error ",err)
		chnl <- mResponse{Body:err.Error(),StatusCode:-1,Seq: seq}
		return
	}
	for i,key := range hKeys{
		req.Header.Set(key,hValues[i])
	}
	//req.Header.Set("Content-Type", "application/json")

	//resp, err := client.Post(URL_ENDPOINT, "application/json", responseBody)
	fmt.Println(" ------- req ",req)
	resp, err := client.Do(req)
	if err != nil {
		s := err.Error()
		if e,ok := err.(net.Error); ok && e.Timeout(){
			fmt.Println("====[GO] Timeout error ",s)
			chnl <- mResponse{Body:err.Error(),StatusCode:-1,Seq: seq}
		}else {
			fmt.Println("====[GO] Other error ",s)
			chnl <- mResponse{Body:err.Error(),StatusCode:-2,Seq: seq}
		}
		log.Printf("====[GO] An Error Occured while making request %v", err)
		return
	}
	defer resp.Body.Close()
	//Read the response body
	body, err := ioutil.ReadAll(resp.Body)
	statusCode := resp.StatusCode
	if err != nil {
		chnl <- mResponse{Body:err.Error(),StatusCode:-3,Seq: seq}
		fmt.Printf("====[GO] An Error Occured while reading response %v",err)
		return
	}
	sb := string(body)
	fmt.Println("====[GO] status code: ",statusCode," response: ",sb)
	res := mResponse{
		Body: sb,
		StatusCode: statusCode,
		Seq : seq }
	chnl <- res
}

//export PostRequests
func PostRequests(url string,payloads []string, headersKey[] string, headersValue [] string, resp []string, statusCode []int)  {
	fmt.Println("input  received len :  {}",len(payloads))
	chnl := make(chan mResponse)
	count := len(payloads)
	start := time.Now()
	for i,payLoad := range payloads {
		//fmt.Printf("hitting request for  %s \n",payLoad)
		go makePostReq(i,url,payLoad,headersKey,headersValue,chnl)
	}
	for ;count >0; {
		res := <- chnl
		resp[res.Seq] = res.Body
		statusCode[res.Seq] = res.StatusCode
		count--
	}
	fmt.Println("====[GO] all requests processed, time took ",time.Since(start))
}


func main() {

}
