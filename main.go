package main

import (
	"flag"
	"fmt"
	"github.com/SpaceStock/Goddard/pkg/scrap"
)

func main(){
	wordStringFlag := flag.String("web", "travelio", "choose website to scrap")

	if(*wordStringFlag == "travelio"){
		result, err := scrap.GetApartments()
		fmt.Println("result: ", result)
		fmt.Println("err:", err)
	}
}
