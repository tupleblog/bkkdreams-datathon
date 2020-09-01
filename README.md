# thai-gov-spending

Thai Government Spending. Visualization for Thai Goverment Spending

We need two files:

``` sh
wget https://raw.githubusercontent.com/425degree-developers/thaiaddress/master/thaiaddress/data/thai_address_data.csv
wget http://www-us.apache.org/dist/pdfbox/2.0.21/pdfbox-app-2.0.21.jar -O pdfbox.jar
```

Use `pdfbox-app-2.0.21.jar` to transform to HTML

``` sh
java -jar pdfbox.jar ExtractText -html budget.pdf budget.html
```
