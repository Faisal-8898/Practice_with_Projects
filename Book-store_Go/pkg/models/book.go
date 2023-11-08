package models

import (
	"book_store/pkg/config"
	"github.com/jinzhu/gorm"
)

var db *gorm.DB

type Book struct {
	gorm.Model
	Name        string `gorm:""json:"name"`
	Author      string `json:"author"`
	Publication string `json:"publication"`
}

func init() {
	config.Connet()
	db = config.GetDb()
	db.AutoMigrate(&Book{})
}

func (b *Book) CreateBook() *Book {
	db.NewRecord(b)
	db.Create(&b)
	return b
}

func GetAllBooks() []Book {
	var Books []Book
	db.Find(&Books)
	return Books
}

func GetBookById(Id int64) (*Book, *gorm.DB) {
	var getbook Book
	db := db.Where("ID=?", Id).Find(&getbook)
	return &getbook, db
}

func DeleteBook(Id int64) Book {
	var book Book
	var deletedBook Book
	db.Where("ID=?", Id).Find(&deletedBook)
	db.Where("ID=?", Id).Delete(book)
	return deletedBook
}
