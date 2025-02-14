import requests

def push_extranet(login, password):

    s = requests.session()

    print('Logging in extranet...')

    data = {
    "__LASTFOCUS":"",
    "__EVENTTARGET":"btnLogin",
    "__EVENTARGUMENT":"",
    "__VIEWSTATE":"/wEPDwUKMjA3NjQzMjE3MA9kFgICAQ9kFgYCAg8PFgYeCENzc0NsYXNzBRJhbGVydCBhbGVydC1kYW5nZXIeBFRleHQFJk9zIGRhZG9zIGluZm9ybWFkb3MgbsOjbyBzw6NvIHZhbGlkb3MhHgRfIVNCAgIWAh4Fc3R5bGUFDmRpc3BsYXk6YmxvY2s7ZAIGDw9kFgIeBXZhbHVlZWQCCQ8PFgIfAQUYSVA6IDxiPjE4Ny45MS4xNjcuMjY8L2I+ZGRkVQVGLVFJTPuTFSZo13OGe7P/4/E=",
    "__VIEWSTATEGENERATOR":"E8460217",
    "__EVENTVALIDATION":"/wEdAAYtQ/VjUYaIoyPhvXK8o5Px3KJmJm/uwlGINQk1yBN0MYN8bMly5ML0Arg3iL2N01FhLuU3Vo6OPqepKDZdTEoXIufUDJ5RlBkXXixesHyU4aKeKEbp39eHc9mbdvkCgxC5ryutq8mxQdoRZ+iUkgtiTnmdAg==",
    "ddTipoUsuario":"DISTRIBUIDOR",
    "txtUsuario":login,
    "txtSenha":password,
    }

    response = s.post('https://www.extranetparker.com.br/estoquedistribuicao/Login.aspx', data=data, verify=False, allow_redirects=False)

    with open('./status_login/session.txt', 'w') as file:
        file.write(response.text)
    file.close()

    response_login = './status_login/session.txt'

    with open(response_login, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 133:

            line_133 = lines[132].strip()

            string_desired = '<option selected="selected" value="DISTRIBUIDOR">DISTRIBUIDOR</option>'

            if line_133 == string_desired:
                result = 'erro_login'
            else:
                result = 'sucess_login'

        file.close()

    if result == 'sucess_login':
        file_extranet = open('./output/export_extranet.csv', "rb")

        data = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$lnkLimparTudo',
        '__EVENTARGUMENT' : '',
        '__VIEWSTATE': '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',
        '__VIEWSTATEGENERATOR': 'D584766B',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': 'nihbrbIYoi0w5wUTcLq7mwN6KZQBp4IyRT4dARdqymODo86Tl8n6KH1nvSoKca5siZEtGbsN6S941deFfuIqpxGPLPA4LNOJwAO5EytzS2iWdMiJ0xxrOJVr/SNhb3Nqd3QwSMg/pP5gecvNX1IlRG9iWrtgN907dIIQpr4SwfslrEiOXRyrD5OWK/KNrBGTqn4+X7EDJN5SrGBsxS869B1ZEZwQEY9Rux12Wlarwu/9NXcwAZl3hyamyUOOCSPjQOgu/41Auj7eCJyYIhn2+IkR3nvAaARyr6oF7xeb5lteK9c4oAazoBO9SCLzZJ5Wc/WfoSObUl4mM4cMTBATje3yMmatkALOWOn5FLPdJFnZyCZS+1C4mh7ID/vicXu3xrfWikjtVbIVmPHBwcfGXbDxUTrUn3kZOYW8QVaX+h76jq5QIGVulscar2jptlR4G/r4yyxoTpvXpcp4Id6GICuKSZnLVX/KutOdGTlj0xhFLtg0cYBBqxESphVARMpWU9MnyRyqSArRShy8Nt8ovvgFz2JhJpMgASrrtKuk+83tz+0t7Ph6vEVOv6sX4FSL8CgDKlbVJLURapyAyZ8tFjI53bMICv1MeCtT2Yr70SbBhLJwyTOxyDJCXKVxqp1EnyLF8creCYOhRtWiPh8HzglsrIhg7+VtLfNIE3Czz/wn0sJPsqql7N/QAvJz9+4M8jUySxvtHvqbJGng2KZk8beo/XP+i8+adqtuXwDv7BaT9AsB3shie9lXw65uqoFBI+yOvn/U2N2XQHcTaI8R1OqojokzW6HrFncN7U4zu0eDkevcaLtO2EqNGSsZj1jhTO5fe8DlwkYwzEReGW/y/OFuVAWfGYEg2E4g1EUj8aCR62sV6x5/wAyJ3aPkjfO2WxGRb3XG1fztOwFrWs16C3UjijrBHQo7pUKSw8xUoaBLbsvu',
        'ctl00$ContentPlaceHolder1$txtPesquisa': '',
        'ctl00$ContentPlaceHolder1$EST_S_PARTNUMBER': '',
        'ctl00$ContentPlaceHolder1$EST_I_QTDE': '',
        'ctl00$ContentPlaceHolder1$EST_M_VALOR': '',

        }
        a = s.post('https://www.extranetparker.com.br/estoquedistribuicao/EstoqueCompartilhado_Cadastro.aspx', data=data, verify=False)

        data = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$lnkImportar',
        '__EVENTARGUMENT' : '',
        '__VIEWSTATE': '9F25I8nuWVboGbGbMxRdZdfpnRIrq/zwEME4n8ZWmFGmN2fDbgFZr5nphXUBgJnIlqjG1ZMw+A6+zOPn0jdktWml+2DNhJSPcc4e+ukGEZR3M8WBQbFel4yd4gA4DgSyJEVK/3UdXkmcmu7hAQv1XDDB9jVQ6Lb4YIWBbvVrRBjab4IIvjcYJiFz5Ji4coVgmbwWpvBvKjuMUoWWEKpWkQHtobAtPHdjHSIjmkonuQpUZwIyWmhtaLYITi7WA0cWd5lHeEvjDj3Ur2YgSs3YYuIGWcODU6ZpcZEhAJoHAH+/htmf8ejNVNjrJ5CDhKXEiA2JkD35+No253KtaKJNfuWVqEtnpm5Mh0obEcEjiGP3Lkjt7hvIo9yccd8gFhANEHMZGkRLBg+9LFVxFIO+Ek6ufzaaSfGGip2rm+d2oZnwiikp9T8XIdehcdQMUcBDc+1G4ipZeFEMoUrdBTrytZtY93eAYIqf4DRgAf7O7XkN0a4lDmdiGbfrcqV6IhWOofa1F7YqpYK6CY8MsO9yT83E4YUTgFf3pJ+m4+kNV/Q72TsyI9LKLr+F/qb917+fVxN7RDe2hYcnk8e0myxUbtkngw4t2sJ54f1D5gxit3ovn9mzmzEK36pM6A+KgwDMm4oD3XI12JXdssAuUiG9mujXNDG9B9mioz6yEeQzDr89Um2AsLwWh97aevcEJul+Uaf4cKW90tGSRZaLmeZCB83z9km8mEDBUVhxV17TXi27N15iQ9HK/sKuNzZ3nAS2n/3FrUo9K1svxVJjs5JC+BrnP9NF912Nfd7JS+7IZMoHeBiXFi+yIPwVR+iMgLZjR7Lv/w==',
        '__VIEWSTATEGENERATOR': 'D584766B',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': 'lMk2xQpXWOvH7IqRILmFSSJx3LoacjGtYpaVxidmojwTqrArr3sdSndhSWF0/Z2N+B62qaUhSAJUGc4ZtILyqA5LM1aP1TNbeQbKEdS8BAVn5nYWpAhX/mmk9uIxeY/B9eHH4RcHAyyUvdbIDz8e969ke6k3pClwP4lLvyJCgySNYSWPG9dYAQwT0JO1hlTqOpSG02Mu1E3BygAZoJaaGkqnHc42CbrC3CeVRPtegQpqwLYdrTux0Cq5pz9LHj+DyH94pKldnPseLhhd38xOKX0l/fw=',
        'ctl00$ContentPlaceHolder1$txtPesquisa': '',
        'ctl00$ContentPlaceHolder1$EST_S_PARTNUMBER': '',
        'ctl00$ContentPlaceHolder1$EST_I_QTDE': '',
        'ctl00$ContentPlaceHolder1$EST_M_VALOR': '',

        }
        a = s.post('https://www.extranetparker.com.br/estoquedistribuicao/EstoqueCompartilhado_Cadastro.aspx', data=data, files={'ctl00$ContentPlaceHolder1$oUploadArquivo': file_extranet})
        file_extranet.close()
        print('SSD atualized.')

    else:
        print('Error in login.')
    
    return result