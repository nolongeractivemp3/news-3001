<?php
$badges = json_decode($_GET["badge"], true);
$showextras = false;
if (count($badges) > 2) {
    $showextras = true;
    $extras = array_slice($badges, 2);
    $badges = array_slice($badges, 0, 2);
    $indicator = ["Name" => " +" . count($extras), "Color" => ""];
}

function renderextra($extras)
{
    foreach ($extras as $extra) {
        echo "<span class='mr-2 mb-2 badge badge-outline badge-" .
            $extra["Color"] .
            " '><strong>" .
            $extra["Name"] .
            "</strong></span>";
    }
}
foreach ($badges as $badge) {
    echo "<span class='mr-2 badge badge-outline badge-" .
        $badge["Color"] .
        " '><strong>" .
        $badge["Name"] .
        "</strong></span>";
}

if ($showextras) {
    $extrasTriggerClass = "badge badge-outline cursor-pointer";
    $extrasDropdownClass =
        "dropdown-content z-[100] p-2 shadow-2xl bg-base-200 border border-white/10 rounded-lg " .
        "w-[75vw] left-1/2 -translate-x-1/2 sm:w-max sm:left-auto sm:translate-x-0";
    $extrasContainerClass = "flex flex-wrap justify-start max-w-full sm:max-w-[240px]";

    echo "<div class='dropdown dropdown-hover dropdown-top dropdown-end'>";
    echo "<div tabindex='0' role='button' class='" .
        $extrasTriggerClass .
        "'>  +" .
        count($extras) .
        "</div>";
    echo "<div tabindex='0' class='" . $extrasDropdownClass . "'>";
    echo "<div class='" . $extrasContainerClass . "'>";
    renderextra($extras);
    echo "</div>";
    echo "</div>";
    echo "</div>";
}
