(function($) {
    'use strict';

    let form = $('.form-create-project');
    let url = '/create_project/';

    form.submit((e) =>  {
        e.preventDefault();
        submitForm(url, form).then(response => {

            if (response.project_name) {
                // Management project name in list
                let projectName = $('<li><h4 project-id=' + response.project_id + '>' + response.project_name + '</h4></li>').hide();
                $('.container-create-project').toggleClass('closed');
                $('.project-list').append(projectName);
                projectName.show('normal');

                // Management project detail view
                const containerProjectDetail = $('.container-projects-details');
                containerProjectDetail.empty();
                containerProjectDetail.append(response.template);
                
                // Reload event in the new elements
                projectName.on('click', function () {
                    displayProjectDetails(response.project_id);
                })

                const formDelete = containerProjectDetail.find('#project-detail-'+response.project_id).find('.form-delete-project');
                formDelete.submit(function (e) {
                    let url = '/delete_project/';
                    e.preventDefault();
                    deleteProject(url, $(this));
                })
            } else {
                console.log(response.error);
            }
        });
        form[0].reset();
    });

    // Display the create project form
    const buttonToCreateProject = $('#btn-create-project');
    buttonToCreateProject.on('click', () => {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {
                $(projectDetail[i]).addClass('d-none');
            }
        })
        $('.container-projects-details').toggleClass('d-none');
        $('.container-create-project').toggleClass('closed');
    });
})(jQuery);