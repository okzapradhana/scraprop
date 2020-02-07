package scrap

import (
	"context"
	"io/ioutil"

	"github.com/MontFerret/ferret/pkg/compiler"
	"github.com/MontFerret/ferret/pkg/drivers"
	"github.com/MontFerret/ferret/pkg/drivers/cdp"
	"github.com/MontFerret/ferret/pkg/drivers/http"
)

func GetApartments() ([]byte, error) {
	var path string = "../../queries/travelio.fql"
	cb, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	query := string(cb)

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

	err = ioutil.WriteFile("travelio.json", out, 0600)
	if err != nil {
		return nil, err
	}

	return out, err
}
