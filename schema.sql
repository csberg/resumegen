CREATE TABLE "certifications" (
    "start_date" TEXT NOT NULL,
    "end_date" TEXT,
    "name" TEXT NOT NULL
);
CREATE TABLE "company_role" (
    "start_date" TEXT NOT NULL,
    "end_date" TEXT NOT NULL,
    "company" TEXT NOT NULL,
    "role" TEXT,
    "description" TEXT
);
CREATE TABLE "val_item_class" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "val_item_type" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT
);
CREATE TABLE "item_class" (
    "item_id" INTEGER NOT NULL,
    "item_class_id" TEXT NOT NULL
);
CREATE TABLE "items" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "item_type_id" REAL NOT NULL,
    "company_id" INTEGER NOT NULL,
    "description" TEXT
);
CREATE TABLE "basic_information" (
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    "phone_number" TEXT NOT NULL
);
