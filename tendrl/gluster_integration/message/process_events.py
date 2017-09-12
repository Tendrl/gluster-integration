from tendrl.gluster_integration.sds_sync import event_utils


POST_RECOVERY_TTL = 200
NOTIFICATION_TTL = 86400   # one day


def process_events():
    events = NS.gluster.objects.NativeEvents().load_all()
    for event in events:

        if event.severity == "recovery" and not event.recovery_processed:
            # this perticular event is recovery event
            # so process this event and delete it
            event_utils.emit_event(
                event.context.split("_")[0],
                event.current_value,
                event.message,
                event.context,
                "INFO"
            )
            processed_event = NS.gluster.objects.NativeEvents(
                event.context,
                recovery_processed=True
            )
            processed_event.save(ttl=POST_RECOVERY_TTL)
            continue

        if event.alert_notify and not event.processed:
            event_utils.emit_event(
                event.context.split("_")[0],
                event.current_value,
                event.message,
                event.context,
                "INFO",
                alert_notify=event.alert_notify
            )
            processed_event = NS.gluster.objects.NativeEvents(
                event.context,
                processed=True
            )
            processed_event.save(NOTIFICATION_TTL)
            continue

        if event.severity == "warning" and not event.processed:
            event_utils.emit_event(
                event.context.split("_")[0],
                event.current_value,
                event.message,
                event.context,
                "WARNING"
            )
            processed_event = NS.gluster.objects.NativeEvents(
                event.context,
                processed=True
            )
            processed_event.save()
            continue
