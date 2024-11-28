import pyshark
import traceback

def search_tls(filename_in, params, filter):
    tls_streams = []
    with pyshark.FileCapture(filename_in, custom_parameters=params, keep_packets=False, debug=False, display_filter=filter) as capture:
        for packet in capture:
            try:
                tls_streams.append(int(packet.tcp.stream))
            except AttributeError:
                print(traceback.format_exc())
    #print(tls_streams)
    return tls_streams

def parse_stream(filename_in, filename_out, tls_streams, params):
    with open(filename_out, "a") as out:
        out.write("TAG: {}".format(filename_in))
        for stream_number in tls_streams:
            out.write("\nstream number: {}\n".format(stream_number))
            with pyshark.FileCapture(filename_in, custom_parameters=params, keep_packets=False, debug=False, display_filter="tcp.stream eq %d and tls" % stream_number) as capture:
                for packet in capture:
                    if 'TLS' in packet:
                        try:
                            tls_type = packet.tls.record_content_type
                            if tls_type == "22":
                                hdsk_type = packet.tls.handshake_type
                                out.write("{}".format(tls_type))
                                for field in hdsk_type.all_fields:
                                    out.write(":{}".format(field.show))
                                out.write(" ")
                            else:
                                out.write("{} ".format(tls_type))
                        except AttributeError:
                            print("attribute error: {}".format(packet.number))
        out.write("\n")

def parse_file(filename_in, filename_out, filter):
    params = ["-o", "tcp.desegment_tcp_streams:TRUE",
        "-o", "tls.desegment_ssl_records:TRUE",
        "-o", "tls.desegment_ssl_application_data:TRUE"]
    #filter = 'tls.handshake.type eq 1 and not (tls.handshake.extensions_server_name matches ".*.microsoft.com|.*.msedge.net|.*.xboxlive.com|.*.bing.com|.*.live.com|.*.windows.com")'

    tls_streams = search_tls(filename_in, params, filter)
    parse_stream(filename_in, filename_out, tls_streams, params)


#content types:
#20 change cipher spec
#21 alert
#22 handshake
#23 application data
#24 heartbeat

#handshake:
#0 hello request
#1 client hello
#2 server hello
#4 new session ticket
#8 encrypted extensions (1.3 only)
#11 certificate
#12 server key exchange
#13 certificate request
#14 server hello done
#15 certificate verify
#16 client key exchange
#20 finished
