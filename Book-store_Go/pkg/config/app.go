package config

import (
	"fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
)

var (
	db *gorm.DB
)

func Connet() {
	dataSourceName := "newuser:password@/book?charset=utf8&parseTime=True&loc=Local"
	d, err := gorm.Open("mysql", dataSourceName)
	if err != nil {
		fmt.Println(err)
		panic("failed to connect database")
	}
	db = d
}
func GetDb() *gorm.DB {
	return db

}
