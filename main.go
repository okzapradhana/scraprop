package main

import (
	"flag"
	"github.com/SpaceStock/Goddard/pkg/scrap"
)

func main(){
	wordStringFlag := flag.String("web", "travelio", "choose website to scrap")

	if(*wordStringFlag == "travelio"){
		scrap.GetApartments()
	}
}