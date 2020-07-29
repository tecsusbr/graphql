let def = {
    liveSearch : true,
    maxOptions : 1,
    noneResultsText: 'Nenhum campo encontrado!',
    width : '100%',
};

let table_language = {
        "sEmptyTable": "Nenhum registro encontrado",
        "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
        "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
        "sInfoFiltered": "(Filtrados de _MAX_ registros)",
        "sInfoPostFix": "",
        "sInfoThousands": ".",
        "sLengthMenu": "_MENU_ resultados por página",
        "sLoadingRecords": "Carregando...",
        "sProcessing": "Processando...",
        "sZeroRecords": "Nenhum registro encontrado",
        "sSearch": "Buscar",
        "oPaginate": {
            "sNext": "Próximo",
            "sPrevious": "Anterior",
            "sFirst": "Primeiro",
            "sLast": "Último"
        },
        "oAria": {
            "sSortAscending": ": Ordenar colunas de forma ascendente",
            "sSortDescending": ": Ordenar colunas de forma descendente"

        }
    };

function load_select() {
    $.ajax({
        url: "http://127.0.0.1:5000/graphqljs",
        contentType: "application/json", type: 'POST',
        data: JSON.stringify({
            query: `
          {
             allDepartments{
                edges{
                    node{
                        deptNo
                        deptName
                    }
                }
             }
          }`
        }),
        success: function (result) {
            if (result['data'] != undefined) {
                html = '<option value=""></option>'
                for (const i of result['data']['allDepartments']['edges']) {
                    html += '<option value="' + i['node']['deptNo'] + '">' + i['node']['deptName'] + '</option>';
                }
                $("#det").html(html).selectpicker('refresh');
            } else {
                console.log(JSON.stringify(result))
            }
        },
        error: function (result) {
            console.log(result)
        }
    });
}

function change_select(){
    if ($("#det").val()=="")
        return ;

        let val = $("#det").val();
        $.ajax({
        url: "http://127.0.0.1:5000/graphqljs",
        contentType: "application/json", type: 'POST',
        data: JSON.stringify({
            query: `
          {
              employeeByDept(dptoNo : "${val}"){
                  firstName
                  lastName
                  countSalary
              }
          }`
        }),
        success: function (result) {
            if (result['data'] != undefined) {
                console.log(result['data']);
                let html = '';
                let th = '';
                for (const items of result['data']['employeeByDept']) {
                    html += '<tr>';
                    if (th == '')
                        for (var key in items) {
                            th += '<th>'+key+'</th>';
                        }

                    for (var key in items)
                        html  += '<td>'+items[key]+'</td>';
                    html += '</tr>';
                }
                $(".card_div").html(`
                    <table id="mytable" >
                        <thead>
                            <tr>${th}</tr>
                        </thead>
                        <tbody>
                            ${html}
                        </tbody>
                    </table>`);
                $('#mytable').DataTable();
            } else {
                console.log(JSON.stringify(result))
            }
        },
        error: function (result) {
            console.log(result)
        }
    });
}