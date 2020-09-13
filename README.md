# Bangkok Datathon (แงะงบกรุงเทพ)

โปรเจกต์นี้เป็นโปรเจกต์จากงานแงะงบกรุงเทพฯปี 2563 จัดที่ BACC

เราได้นำข้อมูลงบของกรุงเทพมหานครในรูปแบบของไฟล์ PDF มาทำให้เป็นข้อมูลตารางและ
ออกแบบแบบสอบถามจากข้อมูลงบกรุงเทพฯ เพื่อทำให้คนที่เข้ามาดูข้อมูลสามารถออกความเห็น
เกี่ยวกับงบประมาณของจังหวัดได้

สามารถดู demo ได้ที่ [https://tupleblog.github.io/bkkdreams-datathon](https://tupleblog.github.io/bkkdreams-datathon/)
(demo นี้ใช้สำหรับเป็นตัวอย่างเท่านั้น ยังไม่ใช่แอพพลิเคชั่นจริงของทางงาน)

## External files

``` sh
wget https://raw.githubusercontent.com/425degree-developers/thaiaddress/master/thaiaddress/data/thai_address_data.csv
wget http://www-us.apache.org/dist/pdfbox/2.0.21/pdfbox-app-2.0.21.jar -O pdfbox.jar
```

Use `pdfbox-app-2.0.21.jar` to transform to HTML

``` sh
java -jar pdfbox.jar ExtractText -html budget.pdf budget.html
```

## Data and website

We store cleaned data in `data` folder and we use `docs` folder to display our website.
We will update ourcode to clean the PDF file later on (we haven't cleaned it due to
the time constraint).
