(function($) {
    'use strict';

    // Event to display the form to create a list
    const btnAddList = $('#btn-create-list');
    btnAddList.on('click', function () {
        $('.create-list').toggleClass('d-none');
    })

    // Event to create list
    let formCreate = $('.form-create-list');
    let url = '/create_list/'
    formCreate.submit((e) => {
        e.preventDefault();
        
        submitForm(url, formCreate).then(response => {
            if (response.list_name) {
                const containerLists = $('.container-project-list');
                containerLists.append(response.template);

                // Reload event with the new elements
                const formDelete = containerLists.find('#project-list-'+response.list_id).find('.form-delete-list');
                formDelete.submit(function (e) {
                    let url = '/delete_list/'
                    e.preventDefault();
                    deleteList(url, $(this));
                })
            }
        })
    })
    formCreate[0].reset();

})(jQuery);