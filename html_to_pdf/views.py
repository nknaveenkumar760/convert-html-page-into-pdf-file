import pdfkit
import wget
from django.shortcuts import render, HttpResponse
from selenium import webdriver


def index(request):

    return render(request,'index.html')


def converter(request):

    try:
        url = request.POST.get('url')
        print(url)
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)

        links = []
        all_link = driver.find_elements_by_xpath("//*[@href]")
        try:

            for i in all_link:
                url_data = i.get_attribute('href')
                print(url_data)
                links.append(url_data)
        except Exception:
            pass
        try:
            for link in links:
                print(link)
                file_name =link.rsplit('/', 1)[-1]
                print(file_name)
                if link:
                   pdf = pdfkit.from_url(link , file_name+'.pdf')
                   wget.download(pdf)
                   print("html page converted in pdf successfully")
                   message = "html page converted in pdf successfully"
                else:
                    print("Enter url....")
                    message = "Please Enter url........"
        except Exception:
            pass

            return render(request,'index.html',{'message':message})

    except IOError:
        pass
        print("IOError occure")
    except ValueError:
        pass
        print("ValueError occur")


def single_url(request):

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }


    try:
        link = request.POST.get('url')
        print(link)
        file_name = link.rsplit('/', 1)[-1]
        print(file_name)
        if link:
            pdf = pdfkit.from_url(link, False, options)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename = "' + file_name + '.pdf"'
            return response
    except Exception:
            pass
