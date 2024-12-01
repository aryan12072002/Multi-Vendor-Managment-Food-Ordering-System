let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
}





$(document).ready(function(){
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');
        data={
            'food_id':food_id,
        }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success:function(response){
                if(response.status=='login_required'){
                    swal (response.message,'','info').then(function(){
                        window.location='/accounts/login';
                    })
                }else if(response.status=='Failed'){
                    swal (response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    subtotal,tax,total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
    
                    ) 
                    

                }
                
            }
        })
        
    })
    //place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id=$(this).attr('id')
        var qty=$(this).attr('data-qty')
        $('#' +the_id).html(qty)
    })

    //descrease cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');
        data={
            'food_id':food_id,
        }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success:function(response){
                if(response.status=='login_required'){
                    swal (response.message,'','info').then(function(){
                        window.location='/accounts/login';
                    })
                }else if(response.status=='Failed'){
                    swal (response.message,'','error')

                    }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    //subtotal,tax,total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
    
                        ) 
                    

                }
                
            }
        })
    })
    //delete cart
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        cart_id=$(this).attr('data-id');
        url=$(this).attr('data-url');

        
        $.ajax({
            type:'GET',
            url:url,
            
            success:function(response){
                console.log(response)
                if(response.status=='Failed'){
                    swal(response.message,'','error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,response.message,"success")
                    //subtotal,tax and grand total
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax_dict'],
                    response.cart_amount['grand_total'],

                    ) 
                    
                    removeCartItem(response.qty,cart_id);
                    checkEmptyCart();

                                
                }
                
            }
        })
    })
    //delete the cart element if the qty is 0
    function removeCartItem(cartItemQty,cart_id){
        if(cartItemQty<=0){
            //remove the cart item element
            document.getElementById("cart-item" +cart_id).remove()


        }
    }
    //check if the cart is empty
    function checkEmptyCart(){
        var cart_counter=document.getElementById('cart_counter').innerHTML
        if(cart_counter==0){
            document.getElementById('empty-cart').style.display="block";
        }
    }
    //apply cart amounts
    function applyCartAmounts(subtotal,tax_dict,grand_total){
        if(window.location.pathname=='/cart/'){
            $('#subtotal').html(subtotal)
            $('#grand_total').html(grand_total)
           
            for (key1 in tax_dict){
                for (key2 in tax_dict[key1]){
                    
                   $('#tax-'+key1).html(tax_dict[key1][key2])
                }

            }

        }
    }

});