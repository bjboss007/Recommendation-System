var table = $('#userTable').DataTable({
    language: {
        search: "_INPUT_",
        searchPlaceholder: "Search records",
        processing: "<i class='fa fa-spinner fa-spin'/>"
    },
    dom:  't l p f',
    lengthMenu: [[5, 10, -1], [5, 10, "All"]],
    pagingType: "full_numbers",
    searching: true,
    rowId: "name",
    processing: true,
    searchDelay: 1500,
    serverSide: true,
    responsive: true,
    ordering: false,
    columns: [
        {data: "username"},
        {data: "arm"},
        {data: "IQ"},
        {data: "career"},
        {data: "re_course"},
    ],
    ajax: {
        url: "/admin/list-users",
        type: "GET"
    }
});

