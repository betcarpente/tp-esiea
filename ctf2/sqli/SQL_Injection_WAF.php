<?php
$db = new SQLite3('users.db');


$db->exec("CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)");

$db->exec("INSERT OR IGNORE INTO users (id, username, password, role) VALUES
    (1, 'admin', 'supersecret', 'admin'),
    (2, 'user',  'password',    'user')
");



function filtrer($input) {
    $input = str_replace(";", "", $input);
    return $input;
}

$msg = "";

if (!empty($_POST['user']) && !empty($_POST['pass'])) {

    $u = filtrer($_POST['user']);
    $p = filtrer($_POST['pass']);

    $query = "SELECT * FROM users WHERE username='$u' AND password='$p'";
    echo "<pre>DEBUG SQL : $query</pre>";
    $res   = $db->query($query);


    if ($row = $res->fetchArray()) {

        $msg .= "Bienvenue, " . htmlspecialchars($row['username']) . "<br>";

        if ($row['role'] === "admin") {
            $msg .= "FLAG : FLAG{WAF_OUAF_OUAF_C_ETAIT_PAS_UN_CHIEN_DE_GARDE}";
        } else {
            $msg .= "Vous n'êtes pas admin, désolé.";
        }

    } else {
        $msg .= "Essaye encore !";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CTF Login</title>
</head>
<body>
    <h2>Connexion</h2>

    <?php if ($msg) echo "<p><b>$msg</b></p>"; ?>

    <form method="POST">
        <input name="user" placeholder="Username" required>
        <br><br>
        <input name="pass" placeholder="Password" type="password" required>
        <br><br>
        <button>Connexion</button>
    </form>
</body>
</html>
