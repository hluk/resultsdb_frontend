$('document').ready(function() {
    // set up the typeahead
    endpoint_url = $('#testcaseEndpointURL').text()
    var testcases = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.nonword,
        queryTokenizer: Bloodhound.tokenizers.nonword,
        prefetch: {
            url: endpoint_url,
            cache: false,
        }
    });

    var start;
    var end;
    var since;

    $('#testcase').typeahead({
        hint: true,
        highlight: true,
        minLength: 0
      },
      {
        name: 'testcases',
        limit: Infinity,
        source: testcases
      }
    );

    // Map the / key to switching the search field
    $(document).bind('keypress', function(e) {
    if(e.keyCode == 47 && !$(":focus").is("input")) //slash key
    {
        e.preventDefault();
        $("#searchButton").click();
    }
    });

    // Focus the item field when search is shown
    $('#collapseSearch').on('shown.bs.collapse', function () {
        $("#item").focus();
    })

    // fill the form based on previous search
    var qs = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=', 2);
            if (p.length == 1)
                b[p[0]] = "";
            else
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));
    console.log(qs);
    if(qs['item']){
        $("#item").val(qs['item']);
    }
    if(qs['item:like']){
        $("#item").val(qs['item:like']);
    }
    if(qs.testcases){
        $("#testcase").val(qs.testcases);
    }
    if(qs.outcome){
        qs.outcome.split(',').forEach(function(item){
            console.log(item);
            $('#outcome option[value="'+item+'"]').attr('selected','selected');
        });
    }

    function date_range(since) {
        if(since){
            var dates = since.replace(' ', '').split(',', 2);
            var start = moment(dates[0], 'YYYY-MM-DD');
            var end = moment();
            if (dates[1]){
                end = moment(dates[1], 'YYYY-MM-DD');
            }
        }else{
            var start = moment().subtract(29, 'days');
            var end = moment();
        }
        return [start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD')]
    };
    var range = date_range(qs.since);
    $("#since").val(range[0] + ',' + range[1]);

    // Replace the submit button behaviour
    $("#searchform").submit(function(e){
        e.preventDefault();

        var url = $("#url").val() + "?";
        var item = $.trim($("#item").val());
        var testcase = $.trim($("#testcase").val());
        var outcome = $("#outcome").val();
        var since = $("#since").val();

        // split the string by whitespace or comma
        items = item.split(/[\s,]+/);
        var item_query = "";
        // for each part add it to the query-string buffer
        items.forEach(function(item){
            item = $.trim(item);
            if(item){
                if(item.indexOf("*") != -1){
                    //wildcard match
                    item_query += item + ",";
                } else {
                    //substring match
                    item_query += item + "*,";
                }
            }
        });
        // if the search contained any item value, add it to overall query url
        if(item_query){
            url+='item:like='+encodeURIComponent(item_query.slice(0, -1));
        }

        if(testcase != 0){
            // split by whitespace or comma
            testcases = testcase.split(/[\s,]+/);

            // check whether like-search is necessary
            var is_like=false;
            testcases.forEach(function(testcase){
                if(testcase.indexOf("*") != -1){
                    is_like=true;
                }
                return $.trim(testcase);
            });
            testcase = testcases.join(',');

            // construct the url
            url += "&testcases";
            if(is_like){
                url += ":like";
            }
            url += "="+encodeURIComponent(testcase);
        }
        if(outcome)
            url += "&outcome="+encodeURIComponent(outcome);

        var range = date_range(since);
        since = range[0] + 'T00:00:00,' + range[1] + 'T23:59:59';
        url += "&since="+encodeURIComponent(since);

        window.location.href = url;
    });
});
