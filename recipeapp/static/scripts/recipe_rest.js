(function($){
	$(document).ready(function(){
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

            // let recipe_description = $('#recipe_desc').sceditor('instance').val().trim();
            let recipe_description = $('#recipe_desc').val().trim();

            if (recipe_description.length == 0) {
                alert('Please provide a recipe description.');
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
	})

})(this.jQuery);