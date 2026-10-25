#!/bin/sh
# Puts GitHub's main (or the commit/branch given as $1) live at https://ft.emil-kirilov.eu: the heimdall jail on
# the home TrueNAS. Local and uncommitted changes are never deployed. The server keeps its own .env and storage/
# (docs/08-signup-server.md).
set -e
cd "$(dirname "$0")"
NAS=root@88.203.194.186
ref=${1:-origin/main}
git fetch -q origin
b=$(mktemp -d)
chmod 755 "$b" # rsync copies it onto the app folder, which www must be able to enter
git archive "$ref" | tar -x -C "$b"
composer install -d "$b" --no-dev --optimize-autoloader --no-interaction --quiet
rsync -rlpt --delete --exclude /.env --exclude /storage/ -e "ssh -p 9022" "$b/" "$NAS:/mnt/raid/iocage/jails/heimdall/root/usr/local/www/followthrough/"
ssh -p 9022 "$NAS" "jexec ioc-heimdall sh -c 'cd /usr/local/www/followthrough && chown -R www:www bootstrap/cache && su -m www -c \"php artisan view:clear -q\"'"
rm -rf "$b"
echo "Deployed $ref ($(git rev-parse --short "$ref")) to https://ft.emil-kirilov.eu"
