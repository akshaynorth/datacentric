(function($){
	$(document).ready(function() {
	    function submit_recipe_search() {
	        let recipe_category = $('#recipe_category').val().trim()
	        if (recipe_category.length == 0) {
	            alert('Please provide a selection for the recipe category')
	            return
	        }

            // Ingredients search is optional
	        let ingredient_list = $('#ingredient_list').val()

	        // Ingredient search type is optional
            let ingredient_search_type = $('#ingredient_search_type').val()

            let form_data = new FormData()

            form_data.append('type', recipe_category)
            if (ingredient_list != null && ingredient_list.length > 0) {
                form_data.append('ingredient_search_type', ingredient_search_type)
                form_data.append('ingredient_list', ingredient_list)
            }

            $.ajax(
            {
                type: 'POST',
                url: '/recipe/search',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    let newDoc = document.open("text/html", "replace")
                    newDoc.write(response)
                    newDoc.close()

                    console.log('Recipe search succeeded')
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not search for recipes. Try again later.')
                }
            }
            )

	    }

        function delete_recipe() {

            $.ajax(
            {
                type: 'POST',
                url: $('delete_recipe').attr('href'),
                data: {},
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    console.log('Recipe delete succeeded')
                    alert('Recipe has been deleted.')
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe deletion failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not delete recipe. Try again later.')
                }
            }
            )
        }

        $('#search_recipe_btn').click(function (e) {
            e.preventDefault()
            submit_recipe_search()
        })

        $('#delete_recipe').click(function (e) {
            e.preventDefault()
            delete_recipe()
        })

	})
})(this.jQuery);