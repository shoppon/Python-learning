set -x

grep "192.168.*ubuntu" /etc/hosts

if [ $? -eq 0 ]; then
    dns=$(dig +short shoppon.site)
    for item in ubuntu freenas js.shoppon.site blog.shoppon.site openwrt.shoppon.site; do
        echo 222333 | sudo -S sed -ie "s#.*${item}#${dns} ${item}#" /etc/hosts
    done
	echo 222333 | sudo -S sed -ie "s#.*\sshoppon.site#${dns} shoppon.site#" /etc/hosts
else
    echo 222333 | sudo -S sed -ie "s#.*ubuntu#192.168.5.77 ubuntu#" /etc/hosts
    echo 222333 | sudo -S sed -ie "s#.*freenas#192.168.5.27 freenas#" /etc/hosts
    echo 222333 | sudo -S sed -ie "s#.*\sshoppon.site#192.168.5.89 shoppon.site#" /etc/hosts
    for item in js.shoppon.site blog.shoppon.site openwrt.shoppon.site; do
        echo 222333 | sudo -S sed -ie "s#.*${item}#192.168.1.4 ${item}#" /etc/hosts
    done
fi