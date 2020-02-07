package main

import (
	"flag"
	"scrap"
)

func main(){
	wordStringFlag := flag.String("web", "travelio", "choose website to scrap")

	if(*wordStringFlag == "travelio"){
		scrap.GetApartments()
	}
}