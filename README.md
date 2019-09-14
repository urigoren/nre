# Nice Regular Expressions

A simple wrapper around the `re` module that supports reuse of patterns.

    import nre
    patterns = nre.from_string(r'''
    number=\d+
    decimal={{number}}\.{{number}}
    lowercase=[a-z]+
    ''')
    print(patterns.decimal.findall("123.22")) # returns ['123.22']
    print(patterns.number.findall("123.22")) # returns ['123', '22']
    print(patterns.decimal.findall("abc"))  # returns []
    print(patterns.lowercase.findall("abc"))  # returns ['abc']
    
 We recommend using external pattern files
 
     import nre
     patterns = nre.from_file("patterns.nre")
 
 If you use external files, you can import them within other files
 
    # contents of users.nre
    valid_username=[a-zA-z_]+
    
    # contents of emails.nre
    import users
    valid_email={{valid_username}}@gmail.com