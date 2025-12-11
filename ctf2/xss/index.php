<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>CTF – XSS Simple</title>
</head>
<body>
    <h2>Bienvenue sur le CTF XSS</h2>

    <p>Envoyez un message :</p>

    <form method="GET">
        <input type="text" name="message" placeholder="Tapez un message…">
        <button type="submit">Envoyer</button>
    </form>

    <hr>

    <p>Votre message :</p>

    <div>
        <?php
            if (isset($_GET['message'])) {
                echo $_GET['message'];
            }
        ?>
    </div>

</body>
</html>