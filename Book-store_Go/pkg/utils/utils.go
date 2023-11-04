package utils

import (
	"encoding/json"
	"net/http"
)

func ParseBody(r *http.Request, x interface{}) error {
	// body, err := io.ReadAll(r.Body)
	// if err != nil {
	// 	return err
	// }
	// err = json.Unmarshal([]byte(body), x)

	err := json.NewDecoder(r.Body).Decode(x)
	if err != nil {
		return err
	}
	return nil
}
