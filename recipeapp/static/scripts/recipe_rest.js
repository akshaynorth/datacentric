(function($){
	$(document).ready(function() {
	    function create_recipe() {
	        // Gather all the information on the generate cooking directions form
            let recipe_label = $('#recipe_label').val().trim()

            if (recipe_label.length == 0) {
                alert('Please provide a recipe label.');
                return;
            }

            let recipe_type = $('#recipe_type').val().trim();
            if (recipe_type.length == 0) {
                alert('Please provide a selection for the recipe type.')
                return;
            }

            let recipe_description = $('#recipe_desc').val().trim();

            if (recipe_description.length == 0) {
                alert('Please provide a recipe description.');
                return;
            }

            let ingredient_list = []
            $('input[name="ingredient_name"]').each(
                function() {
                    ingredient_list.push($(this).val())
                }
            );

            for (i in ingredient_list) {
                if (ingredient_list[i].trim().length == 0) {
                    alert('Provide an ingredient description for each of added ingredients');
                    return;
                }
            }

            let instruction_list = []
            $('input[name="instruction_desc"]').each(
                function() {
                    instruction_list.push($(this).val())
                }
            );

            for (i in instruction_list) {
                if (instruction_list[i].trim().length == 0) {
                    alert('Provide an instruction description for each of added instructions');
                    return;
                }
            }

            let prep_time = $('#prep_time').val().trim()
            if (prep_time.length == 0) {
                alert('Provide a preparation time');
                return;
            }

            let cook_time = $('#cook_time').val().trim();
            if (cook_time.length == 0) {
                alert('Provide the cooking time');
                return;
            }

            let calories = $('#calories').val().trim();
            if (calories.length == 0) {
                alert('Provide the recipe calories');
                return;
            }
	        // Send a request to the flask application to create the recipe
	    }

	    $('#create_recipe_btn').click(function(e) {
	        e.preventDefault();
            create_recipe();
	    });

	    $(':file').change(function(e) {
	        e.preventDefault();
	        if (this.files.length > 0) {
	            $('#upload_picture_filename').text(this.files[0].name);
	        }
	    });

        $.post({
            url: '/recipe/create',
            data: {
                name: recipe_label,
                type: recipe_type,
                prep_time: prep_time,
                recipe_desc: recipe_description,
                cook_time: cook_time,
                calories: calories,
                ingredients: ingredient_list,
                instructions: instruction_list,
            },
            dataType: 'json',
        }).done(
            function() {
                console.log('Recipe submitted');
            }
        ).fail(
            function() {
                console.log('Recipe creation failed')
            }
        )

	})

})(this.jQuery);