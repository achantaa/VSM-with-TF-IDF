from calc import search_result


def print_options():
    """
    Method to print user options onto screen
    :return: None
    """
    print('--------------------********************--------------------')
    print('                 --Choose type of Search--')
    print('                 1 : Search by Title')
    print('                 2 : Search by Author')
    print('                 3 : Search by Description')
    print('                 4 : Search by Year of Publication')
    print('--------------------********************--------------------')
    print('\n--Use "quit" to exit--\n')

if __name__ == '__main__':
    try:
        print("Hello There!\n")
        #print("General Kenobi!!")
        while(True):
            print_options()
            option = input()
            
            if option == 'quit':
                print('\nbye\n')
                break
            option = int(option)
            print('\nEnter Search Query : ')
            query = input()
            print()
            res = search_result(query, option)
            count = 1
            print()
            if option == 1:
                for w in res:
                    print(str(count) + '.', "'" + w[0] + "'" + '\n Score: ' + str('%.5f' %(list(w)[1])) + '\n')
                    count += 1

            elif option == 2:
                for title, author in res.items():
                    if list(title)[1] != 0:
                        print(str(count) + '.', list(title)[0], '\n  Score: ' + str('%.5f' %(list(title)[1])), '\n  ' + list(author)[0]+ '\n')
                        count += 1

            elif option == 3:
                for title, descrip in res.items():
                    print(str(count) + '.', list(title)[0], '\n  Score: ' + str('%.5f' %(list(title)[1])), '\n  ' + list(descrip)[0]+ '\n')
                    count += 1

            elif option == 4:
                for title, year in res.items():
                    if (count <= 10):
                        print(str(count) + '.', str(title) + '\n Year : ' + str(year) + '\n')
                    count += 1
    except:
        print('\nInterrupted.')