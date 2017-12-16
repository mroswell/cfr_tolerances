import scraperwiki
import lxml.html
import re


import csv

target_commodities = ["Poultry, fat","Poultry, meat", "Poultry, meat byproducts", "Hog, fat","Hog, meat", "Hog, meat byproducts", "Cattle, fat","Cattle, meat", "Cattle, meat byproducts", "Egg", "Milk, fat"]
target_commodities = ["Poultry, fat","Poultry, kidney", "Poultry, meat", "Poultry, meat byproducts", "Hog, fat", "Hog, kidney", "Hog, liver", "Hog, meat", "Hog, muscle", "Hog, meat byproducts", "Cattle, fat", "Cattle, kidney", "Cattle, liver", "Cattle, meat", "Cattle, muscle", "Cattle, meat byproducts", "Egg", "Milk, fat"]

url_base= 'https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=1&SID=0d522d57c79aa7c6bd629bce51d61a7f&h=L&mc=true&n=pt40.26.180&r=PART&ty=HTML'
html = scraperwiki.scrape(url_base)
rt = lxml.html.fromstring(html)
results = rt.xpath("//*[@id='browse-layout-mask']/a[count(preceding-sibling::p[@class='contentsp'])=3]")
result_list = []

for c in results:
    result = {}
    href= c.attrib['href']
    title = c.text.replace(u'\xa0', ' ').encode('utf-8')
    title_array = re.split(r'\s{3,}', title)
    title_array1 = re.split(r'; ',title_array[1])

    result['chemical'] = title_array1[0]
    result['url'] = url_base + href
    commodity_section_xpath = "//a[@name='" + href[1:] + "']"
    for v in range(1, 3):
        
        commodity_general_section = rt.xpath(commodity_section_xpath + "/following-sibling::p[1]")
        commodity_table_section_xpath = commodity_section_xpath + "/following-sibling::div["+ str(v) +"]/div[@class='gpotbl_div']/table"
        commodity_table_section = rt.xpath(commodity_table_section_xpath)
        if not commodity_table_section:
            continue
        theader_xpath = commodity_table_section_xpath + "/tr[th[@class='gpotbl_colhed' and contains(., 'Parts per million')]]"
        theader = rt.xpath(theader_xpath)
        if theader:
            result['table_header'] = "parts per million"
        else:
            result['table_header'] = "parts per billion"

        for commodity in target_commodities:
            y = commodity_table_section_xpath + "/tr[td[contains(., '" + commodity + "')]]"
            row = rt.xpath(y)
            for l in row:
                first_td = y + "/td[1]"
                second_td = y + "/td[2]"
                commod = rt.xpath(first_td)[0].text_content()
                if commod in target_commodities:
                    commod_value = rt.xpath(second_td)[0].text_content()
                    result[commod] = commod_value
    chem_type = rt.xpath(commodity_section_xpath + "/following-sibling::p[contains(., 'General.')][1]") 
    if chem_type:
        chem_type = chem_type[0].text_content()

        m = r'residues of ([\w\s\,]+) ' + re.escape(result['chemical'])
        l = re.search(m, chem_type, re.IGNORECASE)
        if l:
            chem_type = l.group(1)
            chem_type = chem_type.replace("the", "").replace(",", "").strip()
        else:
            chem_type = ""
    else:
        chem_type = ""

    result['chem_type'] = chem_type
    print(result['chemical'], result['url'])
    result_list.append(result)

with open('result_output.csv', 'w') as csvfile:
    fieldnames = ['chemical', 'chem_type', 'table_header'] + target_commodities + ['url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for k in result_list:
        writer.writerow(k)
