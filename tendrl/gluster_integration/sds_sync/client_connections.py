import etcd

from tendrl.commons.utils import etcd_utils


def sync_volume_connections(volumes):
    for volume in volumes:
        subvol_count = 0
        vol_connections = 0
        while True:
            try:
                subvol = etcd_utils.read(
                    "clusters/%s/Volumes/%s/Bricks/subvolume%s" % (
                        NS.tendrl_context.integration_id,
                        volume.vol_id,
                        subvol_count
                    )
                )
                if subvol:
                    for entry in subvol.leaves:
                        brick_name = entry.key.split("/")[-1]
                        fetched_brick = NS.tendrl.objects.GlusterBrick(
                            NS.tendrl_context.integration_id,
                            brick_name.split(":")[0],
                            brick_name.split(":_")[-1]
                        ).load()
                        if fetched_brick and fetched_brick.client_count:
                            vol_connections += 0 \
                                if fetched_brick.client_count == '' \
                                else int(fetched_brick.client_count)
                    subvol_count += 1
            except etcd.EtcdKeyNotFound:
                break
        volume.client_count = vol_connections
        volume.save()
