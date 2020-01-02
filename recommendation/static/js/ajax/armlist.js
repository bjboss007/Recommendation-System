var table = $('#armRow').DataTable({
    language: {
        search: "_INPUT_",
        searchPlaceholder: "Search records",
        processing: "<i class='fa fa-spinner fa-spin'/>"
    },
    dom:  't l p f',
    lengthMenu: [[5, 10, -1], [5, 10, "All"]],
    pagingType: "full_numbers",
    searching: true,
    rowId: "id",
    processing: true,
    searchDelay: 1500,
    serverSide: true,
    responsive: true,
    ordering: false,
    columns: [
        {data: "name"},
        {data:null}

    ],
    "columnDefs" : [
        {
            "targets" :1,
            "data" : "operations",
            className :"text-right",
            "render" : function (data, type, row) {
                lbl = '';
                if (type === 'display' ) {
                    kk=`<a href="/admin/${row.id}/add-subjects" class="btn btn-info"> Edit </a>`
                    return kk;
                }
                return data;
               
            }

        }],
    ajax: {
        url: "/admin/list-arms",
        type: "GET"
    }
});

$("#armRow").on('search.dt', function(){
    var value = $('.dataTables_filter input').val()
    table.search(value).draw()
    console.log(value)
})