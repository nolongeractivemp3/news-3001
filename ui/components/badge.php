<?php
$badges = json_decode($_GET["badge"], true);
foreach ($badges as $badge) {
    echo "<span class='mr-2 badge badge-soft badge-" .
        $badge["Color"] .
        " '><strong>" .
        $badge["Name"] .
        "</strong></span>";
}
?>
