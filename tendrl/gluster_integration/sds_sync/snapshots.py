def sync_volume_snapshots(volumes, ttl):
    index = 1
    while True:
        s_index = 1
        try:
            vol_id=volumes['volume%s.id' % index]
            while True:
                try:
                    vol_snapshot = NS.gluster.objects.Snapshot(
                        vol_id=vol_id,
                        id=volumes[
                            'volume%s.snapshot%s.id' % (index, s_index)
                        ],
                        name=volumes[
                            'volume%s.snapshot%s.name' % (index, s_index)
                        ],
                        created_at=' '.join(volumes[
                            'volume%s.snapshot%s.time' % (index, s_index)
                        ]),
                        description=volumes[
                            'volume%s.snapshot%s.description' % (index, s_index)
                        ],
                        status=volumes[
                            'volume%s.snapshot%s.status' % (index, s_index)
                        ]
                    )
                    vol_snapshot.save(ttl=ttl)
                    s_index += 1
                except KeyError:
                    break
            index += 1
        except KeyError:
            break
