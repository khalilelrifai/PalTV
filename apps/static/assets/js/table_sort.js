$(document).ready(function () {
    $('th').on('click', function () {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
        this.asc = !this.asc;
        table.find('th i').removeClass('fa-sort-up fa-sort-down'); // Reset all icons
        if (this.asc) {
            rows.reverse();
            $(this).find('i').removeClass('fa-sort-up').addClass('fa-sort-down');
        } else {
            $(this).find('i').removeClass('fa-sort-down').addClass('fa-sort-up');
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i]);
        }
    });

    function comparer(index) {
        return function(a, b) {
            var valA = getCellValue(a, index);
            var valB = getCellValue(b, index);

            // Convert to numeric values for comparison
            if (!isNaN(valA) && !isNaN(valB)) {
                return valA - valB;
            } else if (valA instanceof Date && valB instanceof Date) {
                return valA - valB;
            } else {
                return valA.localeCompare(valB);
            }
        };
    }

    function getCellValue(row, index) {
        var cell = $(row).children('td').eq(index);
        var val = cell.text().trim();

        // Parse date if applicable
        var date = Date.parse(val);
        if (!isNaN(date)) {
            return new Date(date);
        }

        // Parse numbers if applicable
        var number = parseFloat(val);
        if (!isNaN(number)) {
            return number;
        }

        // Return text for non-date, non-number values
        return val;
    }
});