import pyshark
import traceback
import ipaddress

def search_tls(filename_in, params, filter):
    tls_streams = []
    with pyshark.FileCapture(filename_in, custom_parameters=params, keep_packets=False, debug=False, display_filter=filter) as capture:
        for packet in capture:
            if 'TLS' in packet:
                try:
                    tls_streams.append(int(packet.tcp.stream))
                except AttributeError:
                    print("packet number: {}".format(packet.number))
                    print(traceback.format_exc())
    return tls_streams

def parse_stream(filename_in, filename_out, tls_streams, params): #in: pcap files, out: lists of tls types
    print("\tparse - parsing file {}".format(filename_in))
    with open(filename_out, "a") as out:
        out.write("TAG: {}".format(filename_in))
        for stream_number in tls_streams:
            out.write("\nstream number: {}\n".format(stream_number))
            with pyshark.FileCapture(filename_in, custom_parameters=params, keep_packets=False, debug=False, display_filter="tcp.stream eq %d and tls" % stream_number) as capture:
                for packet in capture:
                    if 'TLS' in packet:
                        for record in packet.get_multiple_layers("TLS"):#for all TLS records in packet
                            try:
                                content_type = record.record_content_type.show #record content type
                                out.write(content_type)

                                if content_type == "22": #if handshake protocol, find all handshake types
                                    out.write(":{}".format(record.handshake_type.show))
                                    handskape_types = record.handshake_type.alternate_fields
                                    if handskape_types:
                                        for field in handskape_types:
                                            out.write(":{}".format(field.show))

                                other_content_types = record.record_content_type.alternate_fields
                                if other_content_types:
                                    for field in other_content_types:
                                        out.write(",{}".format(field.show))

                                out.write(",")
                            except:
                                #print("attribute error: {}".format(packet.number))
                                pass

                            try:
                                opaque_type = record.record_opaque_type.show
                                out.write(opaque_type)
                                other_opaque_types = record.record_opaque_type.alternate_fields
                                if other_opaque_types:
                                    for field in other_opaque_types:
                                        out.write(",{}".format(field.show))
                                out.write(",")
                            except:
                                pass

                        out.write(" ")

        out.write("\n")

def parse_stream_length(filename_in, filename_out, tls_streams, params): #in: pcap files, out: lists of packet lengths
    print("\tparse - parsing file {}".format(filename_in))
    with open(filename_out, "a") as out:
        out.write("TAG: {}".format(filename_in))
        #i = 0
        for stream_number in tls_streams:
            out.write("\nstream number: {}\n".format(stream_number))
            with pyshark.FileCapture(filename_in, custom_parameters=params, keep_packets=False, debug=False, display_filter="tcp.stream eq %d and tls" % stream_number) as capture:
                for packet in capture:
                    if 'TLS' in packet:
                        try:
                            ########################################
                            r_len = packet.tls.record_length
                            # l = int(r_len)

                            l = int(packet.length)
                            l = l // 150
                            l = l + 1
                            try:
                                if ipaddress.ip_address(packet.ip.src).is_private: #if packet.ip.src is private IP
                                    l = l * -1
                            except:#ipv6 case
                                # if packet.ipv6.src == :
                                #     l = l * -1
                                print("{} - ipv6 address - not supported for length mode".format(packet.number))
                            out.write("{} ".format(l))
                            ########################################
                            # len = []

                            # #r_len = packet.tls.record_length
                            # #lunghezza blocco tls
                            # for record in packet.get_multiple_layers("TLS"):#for all TLS records in packet
                            #     len.append(int(record.record_length))

                            # fields = packet.tls._get_all_fields_with_alternates()

                            # try:
                            #     for field in fields:
                            #         for f in field.alternate_fields:
                            #             if f.name == "tls.record.length":
                            #                 len.append(int(f.show))
                            # except:
                            #     pass

                            # #l = sum(len) // 150 #map packet length to a state (buckets of length 150)
                            # for l in len:
                            #     l = l // 150
                            #     l = l + 1 #fix bug: state 0
                            #     try:
                            #         if ipaddress.ip_address(packet.ip.src).is_private: #if packet.ip.src is private IP
                            #             l = l * -1
                            #     except:#ipv6 case
                            #         if packet.ipv6.src == :
                            #             l = l * -1
                            #         #print("{} - ipv6 address - not supported for length mode".format(packet.number))
                            #     out.write("{},".format(l))

                        except AttributeError:
                            pass

                        #out.write(" ")

        out.write("\n")

def parse_file(filename_in, filename_out, mode):
    params = ["-o", "tcp.desegment_tcp_streams:TRUE",
        "-o", "tls.desegment_ssl_records:TRUE",
        "-o", "tls.desegment_ssl_application_data:TRUE"]
    
    #filter = "tls.handshake.type eq 1" #client hello
    filter = "tls.handshake.type eq 2" #server hello

    flows = 0

    tls_streams = search_tls(filename_in, params, filter)
    flows = flows + len(tls_streams)

    if mode == "type":
        parse_stream(filename_in, filename_out, tls_streams, params) #tls content types
    elif mode == "length":
        parse_stream_length(filename_in, filename_out, tls_streams, params) #packets lengths
    else:
        print("\tparse - invalid parse mode")
        return -1

    return flows


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
