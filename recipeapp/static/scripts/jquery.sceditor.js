/*----------------------------------------------------*/
/*  SCEditor
/*----------------------------------------------------*/

(function($){
	$(document).ready(function(){
		function addIng() {
		    let newElem = null;

		    if ($("table#ingredients-sort tr").is('*')) {
		        newElem = $('table#ingredients-sort tr.ingredients-cont.ing:first').clone();
		    }
		    else {
		        newElem = $('<tr class="ingredients-cont separator"><td class="icon"><i class="fa fa-arrows"></i></td><td><input name="ingredient_name" type="text" class="ingredient" placeholder="" /></td><td class="action"><a title="Delete" class="delete" href="#"><i class="fa fa-remove"></i></a></td></tr>');
		    }

            newElem.find('input').val('');

            let add_to_selector = 'table#ingredients-sort';
            if ($('table#ingredients-sort tbody').is(*)) {
                add_to_selector = 'table#ingredients-sort tbody';
            }

			newElem.appendTo(add_to_selector);
		}

		function addInstruction() {
		    let newElem = null;
		    if ($("table#instructions-sort tr").is('*')) {
		        newElem = $('table#instructions-sort tr.ingredients-cont.ing:first').clone();
		    }
		    else {
                newElem = $('<tr class="ingredients-cont separator"><td class="icon"><i class="fa fa-arrows"></i></td><td><input name="instruction_desc" type="text" class="ingredient" placeholder="" /></td><td class="action"><a title="Delete" class="delete" href="#"><i class="fa fa-remove"></i></a></td></tr>');
		    }

            newElem.find('input').val('');

            let add_to_selector = 'table#instructions-sort'
            if ($('table#instructions-sort tbody').is(*)) {
                add_to_selector = 'table#instructions-sort tbody';
            }

			newElem.appendTo(add_to_selector);
		}

		//sortable table
		var fixHelper =  function(e, tr) {
		    var $originals = tr.children();
		    var $helper = tr.clone();
		    $helper.children().each(function(index)
		    {
		      // Set helper cell sizes to match the original sizes
		      $(this).width($originals.eq(index).width());
		    });
		    return $helper;
		  };
		if ($("table#ingredients-sort").is('*')) {
			$('table#ingredients-sort + .add_ingredient').click(function(e){
				e.preventDefault();
				addIng();
			});

			// remove ingredient
			$('#ingredients-sort .delete').live('click',function(e){
				e.preventDefault();
				$(this).parent().parent().remove();
			});

			$('table#ingredients-sort tbody').sortable({
				forcePlaceholderSize: true,
				forceHelperSize: true,
				placeholder : 'sortableHelper',
				helper: fixHelper,
				zIndex: 999990,
				opacity: 0.6,
				tolerance: "pointer"
			});
        }
			// Adding recipe instructions
        if ($("table#instructions-sort").is('*')) {
			$('table#instructions-sort + .add_ingredient').click(function(e){
				e.preventDefault();
				addInstruction();
			});

			// remove instruction
			$('#instructions-sort .delete').live('click',function(e){
				e.preventDefault();
				$(this).parent().parent().remove();
			});

			$('table#instructions-sort tbody').sortable({
				forcePlaceholderSize: true,
				forceHelperSize: true,
				placeholder : 'sortableHelper',
				helper: fixHelper,
				zIndex: 999990,
				opacity: 0.6,
				tolerance: "pointer"
			});
	 	}
	 	})
})(this.jQuery);