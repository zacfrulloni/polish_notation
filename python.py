# A token is either a valid operator (see below) or an integer in the range -300 to 300 e.g. [“+”, “301”, “3”] is an invalid expression so should return None. However, [“+”, “300”, “3”] is a valid expression
# The valid operators are +, -, *, and /
# The division between two integers always truncates toward zero e.g. 1 / 2 = 0 or 12 / 7 = 1
# If the expression contains a divide by 0 the function should return None
# The input does not always represent a valid arithmetic expression in polish notation e.g. ["+", "-", "3", "4"]
def evaluatePNExpression(polish_notation):
    """
    Evaluate the given List of values in Polish notation.
    Keyword arguments:
    polish_notation: List representing the polish notation expression.
    Returns:
    int or None: The result of the polish notation expression if valid. If not valid, returns None.
    """
    polish_notation=check_leading_zero(polish_notation)
    if isinstance(polish_notation, type(None)):
        return None
    polish_notation=clean_list(polish_notation)
    validate_data_types=validate_data(polish_notation)
    if isinstance(validate_data_types, type(None)):
        return None
    list_validation=validate_list(polish_notation)
    if isinstance(list_validation, type(None)):
        return None
    check_list_type=check_list(polish_notation)
    if isinstance(check_list_type, type(None)):
        return None
    values_validation=validate_list_values(polish_notation)
    if isinstance(list_validation, type(None)) or isinstance(values_validation, type(None)):
        return None
    else:
        result, index_list=get_result(polish_notation)
        if result is None:
            return None
        else:
            new_list=update_list(polish_notation, result, index_list)
            # if list only contains one value, return the result, otherwise execute the function again
            if len(new_list) == 1:
                return int(new_list[0])
            else:
                return evaluatePNExpression(new_list)

def validate_data(polish_notation):
    """
    Iterates over polish_notation list to assert data types are correct.
    Keyword arguments:
    polish_notation: List representing the polish notation expression.
    Returns:
    list or None: Returns polish notation list if valid. If not valid, returns None.
    """
    # iterate over list and convert the following datatypes to strings: int
    for value in polish_notation:
        # check if string contains float number & return none
        if isinstance(value, float) or (isinstance(value, str) and value.count('.') == 1 and value.replace('.', '').isnumeric()) or isinstance(value, int):
            return None
        else:
            pass
    return True

def check_leading_zero(polish_notation):
    """Check if string contains a leading zero and return none if correct else return 
    polish_notation list"""
    for v in polish_notation:
        if v[0]=='0' and v[1].isdigit():
            return None
    else:
        return polish_notation

def check_list(polish_notation):
    """
    If the input is a list returns the list, else returns None.
    keyword arguments:
    polish_notation: List, tuple, set or frozenset representing the polish notation expression
    Returns:
    list: list containing polish notation expression, or None.
    """
    if isinstance(polish_notation, list):
        return polish_notation
    else:
        return None

def clean_list(polish_notation):
    """
    This function removes unwanted symbols from the input list
    keyword arguments:
    polish_notation: List representing the polish notation expression.
    Returns:
    list: Updated polish notation list.
    """
    symbol_list=['(',')','[',']','{','}']
    for symbol in symbol_list:
        if symbol in polish_notation:
            polish_notation.remove(symbol)
    return polish_notation

def validate_list(polish_notation):
    """
    This function validates the length of the polish_notation list
    keyword arguments:
    polish_notation: List representing the polish notation expression
    Returns:
    bool or None: True if valid. If invalid, returns None.
    """
    if len(polish_notation)%2==0 or len(polish_notation)==1 or len(polish_notation)==0 or ('' or ' ' in polish_notation):
        return None
    else:
        return True
    
def validate_list_values(polish_notation):
    """
    This function is used to ensure all integers in the polish notation list are 
    in the range of: -300 to 300 and the list only contains valid values such as digits and operators

    keyword arguments:
    polish_notation: List representing the polish notation expression

    Returns:
    bool or None: True if valid. If invalid, returns None.
    """

    valid_operators=['+','-','/','*']
    for value in polish_notation:
        if value.lstrip("-").isdigit() and (-300 <= int(value) <=300) or value in valid_operators:
            pass
        else:
            return None
    return True

def get_result(polish_notation):
    """This function gets the first 2 adjacent numbers in the polish notation list and verifies there 
    is a valid operator before the first digit. It then places the operator between the 2 digits to
    carry out the operation, the operator and both digits are then removed from the list and the 
    result is pushed into the list. The function is called again until there is only one value in the list
    keyword arguments:
    polish_notation: List representing the polish notation expression
    Returns:
    result or None: Result and index list if valid. If invalid, returns None
    """
    
    # while there is more than 2 strings in the list, keep iterating:
    while len(polish_notation) > 1:
        index_list=[]
        # iterate over list to get first 2 adjacent numbers and the operator
        for index, (operator, first_value, second_value) in enumerate(zip(polish_notation, polish_notation[1:], polish_notation[2:])):
            # check if there are 2 adjacent digits and use lstrip to consider also negative numbers for isdigit()
            if first_value.lstrip("-").isdigit() and second_value.lstrip("-").isdigit():
                # now store the indices of the operator, first_value, second_value in a list to remove these values from the list afterwards.
                index_list.extend([index, index+1, index+2])
                # convert strings to int
                first_number, second_number=int(first_value), int(second_value)
                # return none if the expression contains a divide by zero:
                if operator == '/' and (first_number ==0 or second_number == 0):
                    return None, None
                else:
                    # carry out operation using eval and store value in result, wrap '/' operation in (int) to truncate to zero
                    if operator == '/':
                        result=(int(first_number / second_number))
                    else:
                        result=eval(f'{first_number} {operator} {second_number}')
                    return result, index_list

def update_list(polish_notation, result, index_list):
    """
    This function updates the input list after the first operation is carried out.
    keyword arguments:
    result: result of the operation.
    index_list: List of indices that will be removed from the input list.
    Returns:
    list: Updated list
    """
    # assert result is a string
    result_string=str(result)
    # replace the result with the operator index
    polish_notation[index_list[0]]=result_string
    # remove the first_value and second_value index from the list, must use reverse to pop elements in reverse order
    for index in reversed(index_list[1:]):
        polish_notation.pop(index)
    return polish_notation

if __name__ == "__main__":
    polish_notation=['/','1','0']
    # should be 31
    final_result=evaluatePNExpression(polish_notation)
    print(final_result)