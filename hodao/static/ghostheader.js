/*
** code from : https://dl.dropboxusercontent.com/u/297705/PoC/tableheaderpoc.html
*/

        var currentFixedHeader;
        var currentGhost;
        $(document).scroll(function() {
            $.fn.reverse = [].reverse;

            var createGhostHeader = function (header, topOffset) {
                // Don't recreate if it is the same as the current one
                if (header == currentFixedHeader && currentGhost)
                {
                    currentGhost.css('top', -topOffset + "px");
                    return currentGhost;
                }

                if (currentGhost)
                    $(currentGhost).remove();

                var realTable = $(header).parents('table');

                var headerPosition = $(header).offset();
                var tablePosition = $(realTable).offset();

                var container = $('<table></table>');

                // Copy attributes from old table (may not be what you want)
                for (var i = 0; i < realTable[0].attributes.length; i++) {
                    var attr = realTable[0].attributes[i];
                    container.attr(attr.name, attr.value);
                }

                // Set up position of fixed row
                container.css({
                    position: 'fixed',
                    top: -topOffset,
                    left: tablePosition.left,
                    width: $(realTable).outerWidth()
                });

                // Create a deep copy of our actual header and put it in our container
                var newHeader = $(header).clone().appendTo(container);

                var collection2 = $(newHeader).find('td');

                // TODO: Copy the width of each <td> manually
                $(header).find('td').each(function () {
                    var matchingElement = $(collection2.eq($(this).index()));
                    $(matchingElement).width($(this).width() + 0.5);
                });

                currentGhost = container;
                currentFixedHeader = header;

                // Add this fixed row to the same parent as the table
                $(table).parent().append(currentGhost);
                return currentGhost;
            };

            var currentScrollTop = $(document).scrollTop();

            var activeHeader = null;
            var table = $('table').first();
            var tablePosition = table.offset();
            var tableHeight = table.height();

            var lastHeaderHeight = $(table).find('thead').last().height();
            var topOffset = 0;

            // Check that the table is visible and has space for a header
            if (tablePosition.top + tableHeight - lastHeaderHeight >= currentScrollTop)
            {
                var lastCheckedHeader = null;
                // We do these in reverse as we want the last good header
                var headers = $(table).find('thead').reverse().each(function () {
                    var position = $(this).offset();

                    if (position.top <= currentScrollTop)
                    {
                        activeHeader = this;
                        return false;
                    }

                    lastCheckedHeader = this;
                });

                if (lastCheckedHeader)
                {
                    var offset = $(lastCheckedHeader).offset();
                    if (offset.top - currentScrollTop < $(activeHeader).height())
                        topOffset = $(activeHeader).height() - (offset.top - currentScrollTop) + 1;
                }
            }
            // No row is needed, get rid of one if there is one
            if (activeHeader == null && currentGhost)
            {
                currentGhost.remove();
                currentGhost = null;
                currentFixedHeader = null;
            }

            // We have what we need, make a fixed header row
            if (activeHeader)
                createGhostHeader(activeHeader, topOffset);
        });