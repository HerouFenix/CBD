findNonRepeatingDigits = function () {
    var fullNumber = db.phones.find({},{"display": 1, "_id": 0}).toArray();

    var non_repeating_numbers = []
    for (var i = 0 ; i<fullNumber.length ; i++){
        var number = fullNumber[i].display
        number = number.split("-")[1]
        
        var arr = []
        var non_repeating = true

        for(var j = 0 ; j<number.length ; j++){
            if (arr.includes(number[j])){
                non_repeating = false
                break
            }
            arr.push(number[j])
        }

        if (non_repeating){
            non_repeating_numbers.push(fullNumber[i])
        }
    }

    return non_repeating_numbers
}
    
    