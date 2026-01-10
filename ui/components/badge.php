<?php
$badges = json_decode($_GET["badge"], true);
foreach ($badges as $badge) {
    echo "<span class='badge badge-soft badge-" .
        $badge["Color"] .
        " mr-2'><strong>" .
        $badge["Name"] .
        "</strong></span>";
}
?>
