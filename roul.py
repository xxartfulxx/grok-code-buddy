def
     
    roulette_probability
    (
    target_number
    )
    :


        
    RED_NUMBERS
     
    =
     
    {
    1
    ,
     
    3
    ,
     
    5
    ,
     
    7
    ,
     
    9
    ,
     
    12
    ,
     
    14
    ,
     
    16
    ,
     
    18
    ,
     
    19
    ,
     
    21
    ,
     
    23
    ,
     
    25
    ,
     
    27
    ,
     
    30
    ,
     
    32
    ,
     
    34
    ,
     
    36
    }


        
    BLACK_NUMBERS
     
    =
     
    set
    (
    range
    (
    1
    ,
     
    37
    )
    )
     
    -
     
    RED_NUMBERS


        
    WHEEL
     
    =
     
    [
    0
    ]
     
    +
     
    list
    (
    range
    (
    1
    ,
     
    19
    )
    )
     
    +
     
    [
    37
    ]
     
    +
     
    list
    (
    range
    (
    20
    ,
     
    37
    )
    )
     
    +
     
    [
    38
    ]
      
    # 37 and 38 are placeholders for 00


        
    WHEEL
    .
    extend
    (
    [
    39
    ]
    )
      
    # 39 for 00, if needed


        


        
    # Base probability


        
    base_prob
     
    =
     
    1
    /
    37


        


        
    # Initialize probabilities


        
    probabilities
     
    =
     
    {
    num
    :
     
    base_prob
     
    for
     
    num
     
    in
     
    range
    (
    37
    )
    }


        


        
    if
     
    target_number
     
    not
     
    in
     
    range
    (
    37
    )
    :


            
    raise
     
    ValueError
    (
    "
    Target number must be between 0 and 36
    "
    )


        


        
    # Adjust probabilities based on proximity


        
    target_index
     
    =
     
    WHEEL
    .
    index
    (
    target_number
    )


        
    for
     
    i
    ,
     
    num
     
    in
     
    enumerate
    (
    WHEEL
    )
    :


            
    if
     
    num
     
    ==
     
    target_number
    :
      
    # Skip the target number itself


                
    continue


            
    distance
     
    =
     
    min
    (
    abs
    (
    i
     
    -
     
    target_index
    )
    ,
     
    37
     
    -
     
    abs
    (
    i
     
    -
     
    target_index
    )
    )
      
    # Considering wrap-around


            
    if
     
    distance
     
    >
     
    0
    :
      
    # Avoid adding probability to the target number itself


                
    # Prevent division by zero and ensure small values don't cause issues


                
    probabilities
    [
    num
    ]
     
    +
    =
     
    base_prob
     
    /
     
    (
    distance
     
    *
     
    2
     
    +
     
    1
    )
     




        
    # Normalize probabilities to ensure they sum up to 1


        
    total_prob
     
    =
     
    sum
    (
    probabilities
    .
    values
    (
    )
    )


        
    if
     
    total_prob
     
    ==
     
    0
    :


            
    raise
     
    ValueError
    (
    "
    All probabilities sum to zero, cannot normalize.
    "
    )


        
    for
     
    num
     
    in
     
    probabilities
    :


            
    probabilities
    [
    num
    ]
     
    /
    =
     
    total_prob




        
    # Adjust for color and odd/even


        
    for
     
    num
    ,
     
    prob
     
    in
     
    probabilities
    .
    items
    (
    )
    :


            
    if
     
    num
     
    ==
     
    0
    :


                
    probabilities
    [
    num
    ]
     
    *
    =
     
    1.1
      
    # Slight boost for green 0


            
    elif
     
    num
     
    in
     
    RED_NUMBERS
     
    and
     
    target_number
     
    in
     
    RED_NUMBERS
    :


                
    probabilities
    [
    num
    ]
     
    *
    =
     
    1.05
      
    # Small boost for same color


            
    elif
     
    num
     
    in
     
    BLACK_NUMBERS
     
    and
     
    target_number
     
    in
     
    BLACK_NUMBERS
    :


                
    probabilities
    [
    num
    ]
     
    *
    =
     
    1.05
      
    # Small boost for same color


            
    if
     
    num
     
    %
     
    2
     
    ==
     
    target_number
     
    %
     
    2
    :


                
    probabilities
    [
    num
    ]
     
    *
    =
     
    1.02
      
    # Small boost for same parity


        


        
    # Normalize again after color/odd-even adjustments


        
    total_prob
     
    =
     
    sum
    (
    probabilities
    .
    values
    (
    )
    )


        
    if
     
    total_prob
     
    ==
     
    0
    :


            
    raise
     
    ValueError
    (
    "
    All probabilities sum to zero after adjustments, cannot normalize.
    "
    )


        
    for
     
    num
     
    in
     
    probabilities
    :


            
    probabilities
    [
    num
    ]
     
    /
    =
     
    total_prob


        


        
    return
     
    probabilities




    # Example usage


    try
    :


        
    target
     
    =
     
    17


        
    probs
     
    =
     
    roulette_probability
    (
    target
    )


        
    for
     
    number
    ,
     
    probability
     
    in
     
    probs
    .
    items
    (
    )
    :


            
    print
    (
    f
    "
    Number 
    {
    number
    }
    : 
    {
    probability
    :
    .6f
    }
    "
    )


    except
     
    ValueError
     
    as
     
    e
    :


        
    print
    (
    f
    "
    Error: 
    {
    e
    }
    "
    )



