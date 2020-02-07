package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/MontFerret/ferret/pkg/compiler"
	"github.com/MontFerret/ferret/pkg/drivers"
	"github.com/MontFerret/ferret/pkg/drivers/cdp"
	"github.com/MontFerret/ferret/pkg/drivers/http"
)

func main() {
	apartments, err := getApartments()
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}

	fmt.Print(apartments)
}

func getApartments() ([]byte, error) {
	var path string = "../../queries/travelio.fql"
	contentByte, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	query := string(contentByte)

	comp := compiler.New()
	program, err := comp.Compile(query)
	if err != nil {
		return nil, err
	}

	ctx := context.Background()

	ctx = drivers.WithContext(ctx, cdp.NewDriver())
	ctx = drivers.WithContext(ctx, http.NewDriver(), drivers.AsDefault())

	out, err := program.Run(ctx)
	if err != nil {
		return nil, err
	}

	ioutil.WriteFile("travelio.json", out, 0600)

	return out, err
}
